#pragma once

#include <assert.h>
#include <ATen/ATen.h>
#include <ATen/core/Array.h>
#include <ATen/cuda/CUDAContext.h>
#include <ATen/cuda/detail/OffsetCalculator.cuh>
#include <ATen/detail/FunctionTraits.h>
#include <THC/THCDeviceUtils.cuh>
#include <THC/THCGeneral.hpp>
#include <ATen/native/TensorIterator.h>
#include <ATen/native/cuda/Loops.cuh>
#include <ATen/native/cuda/MemoryAccess.cuh>
#include <c10/macros/Macros.h>
#include <c10/cuda/CUDACachingAllocator.h>
#include <functional>
#include <iosfwd>
#include <tuple>
#include <type_traits>
#include <utility>
#include <thrust/tuple.h>

namespace at { namespace native {

using at::detail::Array;

static inline int64_t div_up(int64_t a, int64_t b) {
  return (a + b - 1) / b;
}

// returns floor(log2(n))
static inline int last_pow2(int n) {
  n |= (n >>  1);
  n |= (n >>  2);
  n |= (n >>  4);
  n |= (n >>  8);
  n |= (n >> 16);
  return std::max(1, n - (n >> 1));
}

// returns reduced fraction numerator & denominator
C10_HOST_DEVICE static void reduce_fraction(size_t &numerator, size_t &denominator) {
  // get GCD of num and denom using Euclid's algorithm.
  // Can replace this with std::gcd if we ever support c++17.
  size_t a = denominator;
  size_t b = numerator;
  while (b != 0) {
      a %= b;
      // swap(a,b)
      size_t tmp = a;
      a = b;
      b = tmp;
  }

  // a is now the GCD
  numerator /= a;
  denominator /= a;
}

struct ReduceConfig {
  static constexpr int BLOCK_X = 0;
  static constexpr int BLOCK_Y = 1;
  static constexpr int CTA = 2;

  static constexpr int MAX_NUM_THREADS = 512;
  static constexpr int vec_size = 4;

  ReduceConfig(int element_size_bytes, int num_outputs, int num_inputs)
    : element_size_bytes(element_size_bytes)
    , num_inputs(num_inputs)
    , num_outputs(num_outputs) {}

  int element_size_bytes;
  int num_inputs;
  int num_outputs;
  int step_input = 1;
  int step_output = 1;
  int ctas_per_output = 1;
  int input_mult[3] = {0, 0, 0};
  int output_mult[2] = {0, 0};

  int block_width;
  int block_height;
  int num_threads;

  bool vectorize = false;

  void set_block_dimension(int64_t dim0, int64_t dim1) {
    int dim0_pow2 = dim0 < MAX_NUM_THREADS ? static_cast<int>(last_pow2(dim0)) : MAX_NUM_THREADS;
    int dim1_pow2 = dim1 < MAX_NUM_THREADS ? static_cast<int>(last_pow2(dim1)) : MAX_NUM_THREADS;
    block_width = std::min(dim0_pow2, int(at::cuda::warp_size()));
    block_height = std::min(dim1_pow2, int(MAX_NUM_THREADS / block_width));
    block_width = std::min(dim0_pow2, int(MAX_NUM_THREADS / block_height));
    num_threads = block_width * block_height;
  }

  int split_input(int parallelism) {
    int step = step_input;
    step_input *= parallelism;
    return step;
  }

  int split_output(int parallelism) {
    int step = step_output;
    step_output *= parallelism;
    return step;
  }

  dim3 block() const {
    return dim3(block_width, block_height);
  }

  dim3 grid() const {
    return dim3(div_up(num_outputs, step_output), ctas_per_output);
  }

  C10_HOST_DEVICE bool should_block_x_reduce() const {
    return input_mult[BLOCK_X] != 0;
  }

  C10_HOST_DEVICE bool should_block_y_reduce() const {
    return input_mult[BLOCK_Y] != 0;
  }

  C10_HOST_DEVICE bool should_global_reduce() const {
    return input_mult[CTA] != 0;
  }

  C10_DEVICE bool should_store(int output_idx) const {
    return output_idx < num_outputs &&
      (!should_block_x_reduce() || threadIdx.x == 0) &&
      (!should_block_y_reduce() || threadIdx.y == 0);
  }

  C10_DEVICE bool should_reduce_tail() const {
    return (!should_block_y_reduce() || threadIdx.y == 0) &&
      (!should_global_reduce() || blockIdx.y == 0);
  }

  C10_HOST_DEVICE int input_idx() const {
    int lane = threadIdx.x;
    int warp = threadIdx.y;
    int cta2 = blockIdx.y;
    return (lane * input_mult[BLOCK_X] +
            warp * input_mult[BLOCK_Y] +
            cta2 * input_mult[CTA]);
  }

  C10_HOST_DEVICE int output_idx() const {
    int lane = threadIdx.x;
    int warp = threadIdx.y;
    int cta1 = blockIdx.x;
    return (lane * output_mult[BLOCK_X] +
            warp * output_mult[BLOCK_Y] +
            cta1 * step_output);
  }

  C10_DEVICE int shared_memory_offset(int offset) const {
    return threadIdx.x + (threadIdx.y + offset) * blockDim.x;
  }

  C10_DEVICE int staging_memory_offset(int cta2) const {
    int offset = cta2 + blockIdx.x * gridDim.y;
    if (!should_block_x_reduce()) {
      offset = threadIdx.x + offset * blockDim.x;
    }
    return offset;
  }

  int shared_memory_size() const {
    if (!should_block_y_reduce() &&
        (!should_block_x_reduce() ||
         block_width <= at::cuda::warp_size())) {
      return 0;
    }
    return element_size_bytes * num_threads;
  }

  int64_t global_memory_size() const {
    if (!should_global_reduce()) {
      return 0;
    }
    auto size = (int64_t)element_size_bytes * num_outputs * ctas_per_output;
    if (!should_block_x_reduce()) {
      size *= block().x;
    }
    return size;
  }

  int semaphore_size() const {
    if (!should_global_reduce()) {
      return 0;
    }
    return sizeof(int) * grid().x;
  }

  int values_per_thread() const {
    return div_up(num_inputs, step_input);
  }
};

std::ostream& operator<<(std::ostream& out, const ReduceConfig& config);

template<int nt, typename R>
C10_LAUNCH_BOUNDS_2(nt, 4)
__global__ void reduce_kernel(R reduction) {
  reduction.run();
}

template <typename index_t>
static OffsetCalculator<2, index_t> make_output_calculator(const TensorIterator& iter) {
  int num_reduce_dims = iter.num_reduce_dims();
  int num_output_dims = iter.ndim() - num_reduce_dims;
  int input_index = iter.ntensors() - 1;
  int output_index = 0;
  std::array<const int64_t*, 2> strides = {
    iter.strides(output_index).data() + num_reduce_dims,
    iter.strides(input_index).data() + num_reduce_dims,
  };
  auto shape = iter.shape().data() + num_reduce_dims;
  return OffsetCalculator<2, index_t>(num_output_dims, shape, strides.data());
}

template <typename index_t>
static OffsetCalculator<1, index_t> make_input_calculator(const TensorIterator& iter) {
  int num_reduce_dims = iter.num_reduce_dims();
  int input_index = iter.ntensors() - 1;
  std::array<const int64_t*, 1> strides = {
    iter.strides(input_index).data(),
  };
  return OffsetCalculator<1, index_t>(num_reduce_dims, iter.shape().data(), strides.data());
}

template <typename out_scalar_t, typename func_t>
struct func_wrapper_t {
  using arg_t = typename binary_function_traits<func_t>::arg1_t;
  using scalar_t = typename binary_function_traits<func_t>::arg2_t;

  func_t combine;
  static inline __device__ out_scalar_t project(arg_t arg) {
    return (out_scalar_t) arg;
  }
  static inline __device__ arg_t warp_shfl_down(arg_t arg, int offset) {
    return WARP_SHFL_DOWN(arg, offset);
  }

  static __device__ arg_t translate_idx(arg_t acc, int64_t /*idx*/) {
    return acc;
  }

  func_wrapper_t(const func_t& op) : combine(op) {
  }

  // wrap a normal reduction that ignores the index
  __device__ arg_t reduce(arg_t acc, scalar_t val, int64_t idx) const {
    return combine(acc, val);
  }
};

template <typename scalar_t, typename func_t>
func_wrapper_t<scalar_t, func_t> func_wrapper(const func_t& op) {
  return func_wrapper_t<scalar_t, func_t> { op };
}

template <typename scalar_t, typename ops_t, typename index_t, typename out_scalar_t=scalar_t, int vt0=4>
struct ReduceOp {
  using traits = function_traits<decltype(&ops_t::reduce)>;
  using arg_t = typename std::decay<typename traits::template arg<0>::type>::type;

  using InputCalculator = OffsetCalculator<1, index_t>;
  using OutputCalculator = OffsetCalculator<2, index_t>;

  static constexpr bool can_accumulate_in_output =
    std::is_convertible<arg_t, out_scalar_t>::value
    && std::is_convertible<out_scalar_t, arg_t>::value;

  static constexpr float acc_buffer_multiplier = (float)sizeof(arg_t) / sizeof(out_scalar_t);

  static constexpr int vec_size = ReduceConfig::vec_size;

  ops_t ops;
  arg_t ident;
  ReduceConfig config;
  InputCalculator input_calc;
  OutputCalculator output_calc;
  const void* src;
  const char* dst[2]; //it accepts at most two destinations
  // acc_buf used for accumulation among sub Tensor Iterator when accumulation on
  // output is not permissible
  void* acc_buf;
  // cta_buf used for accumulation between blocks during global reduction
  void* cta_buf;
  int* semaphores;
  int64_t base_idx;
  bool accumulate;
  bool final_output;
  int noutputs;

  ReduceOp(
      ops_t ops,
      ReduceConfig config,
      InputCalculator input_calc,
      OutputCalculator output_calc,
      const void* src,
      char* dst0,
      optional<char*> dst1,
      void* acc_buf,
      void* cta_buf,
      int* semaphores,
      arg_t ident,
      int noutputs,
      int64_t base_idx)
      : ops(ops),
        ident(ident),
        config(config),
        input_calc(input_calc),
        output_calc(output_calc),
        src(src),
        acc_buf(acc_buf),
        cta_buf(cta_buf),
        semaphores(semaphores),
        base_idx(base_idx),
        noutputs(noutputs) {
    dst[0] = dst0;
    if (dst1.has_value()) {
      dst[1] = dst1.value();
    }
  }

  C10_DEVICE void run() const {
    extern __shared__ char shared_memory[];
    index_t output_idx = config.output_idx();
    index_t input_idx = config.input_idx();
    auto base_offsets = output_calc.get(output_idx);

    arg_t value = ident;

    if (output_idx < config.num_outputs && input_idx < config.num_inputs) {
      const scalar_t* input_slice = (const scalar_t*)((const char*)src + base_offsets[1]);
      value = thread_reduce(input_slice);
    }

    if (config.should_block_y_reduce()) {
      value = block_y_reduce(value, shared_memory);
    }
    if (config.should_block_x_reduce()) {
      value = block_x_reduce(value, shared_memory);
    }

    auto out = (out_scalar_t*)((char*)dst[0] + base_offsets[0]);
    arg_t* acc = nullptr;
    if (acc_buf != nullptr) {
      size_t numerator = sizeof(arg_t);
      size_t denominator = sizeof(out_scalar_t);
      reduce_fraction(numerator, denominator);
      acc = (arg_t*)((char*)acc_buf + (base_offsets[0] * numerator / denominator));
    }

    if (config.should_global_reduce()) {
      value = global_reduce(value, acc, shared_memory);
    } else if (config.should_store(output_idx)) {
      if (accumulate) {
        value = ops.translate_idx(value, base_idx);
      }

      if (acc == nullptr) {
        if (accumulate) {
          value = accumulate_in_output<can_accumulate_in_output>(out, value);
        }
        if (final_output) {
          set_results_to_output(value, base_offsets[0]);
        } else {
          *out = get_accumulated_output<can_accumulate_in_output>(out, value);
        }
      } else {
        if (accumulate) {
          value = ops.combine(*acc, value);
        }
        if (final_output) {
          set_results_to_output(value, base_offsets[0]);
        } else {
          *acc = value;
        }
      }
    }
  }

  C10_DEVICE arg_t thread_reduce(const scalar_t* data) const {
    if (config.vectorize) {
      // reduce at the header of input_slice where memory is not aligned,
      // so that thread_reduce will have an aligned memory to work on.
      return vectorized_thread_reduce_impl(data);
    } else {
      index_t element_stride = input_calc.strides_[0][0] / sizeof(scalar_t);
      bool is_contiguous = (input_calc.dims == 1 && element_stride == 1);
      if (is_contiguous) {
        return thread_reduce_impl(data, [](index_t idx) { return idx; });
      } else if (input_calc.dims == 1) {
        return thread_reduce_impl(data, [&](index_t idx) { return idx * element_stride; });
      } else {
        return thread_reduce_impl(data, [&](index_t idx) { return input_calc.get(idx)[0] / sizeof(scalar_t); });
      }
    }
  }

  C10_DEVICE arg_t vectorized_thread_reduce_impl(const scalar_t* data) const {
    index_t end = config.num_inputs;

    // Handle the head of input slice where data is not aligned
    arg_t value = ident;
    constexpr int align_bytes = alignof(at::native::memory::aligned_vector<scalar_t, vec_size>);
    constexpr int align_elements = align_bytes / sizeof(scalar_t);
    int shift = ((uint64_t)data) % align_bytes / sizeof(scalar_t);
    if (shift > 0) {
      data -= shift;
      end += shift;
      if(threadIdx.x >= shift && threadIdx.x < align_elements && config.should_reduce_tail()){
        value = ops.reduce(value, data[threadIdx.x], threadIdx.x - shift);
      }
      end -= align_elements;
      data += align_elements;
      shift = align_elements - shift;
    }

    // Do the vectorized reduction
    using load_t = at::native::memory::aligned_vector<scalar_t, vec_size>;

    index_t idx = config.input_idx();
    const index_t stride = config.step_input;

    // Multiple accumulators to remove dependency between unrolled loops.
    arg_t value_list[vec_size];
    value_list[0] = value;
    #pragma unroll
    for (int i = 1; i < vec_size; i++) {
      value_list[i] = ident;
    }

    scalar_t values[vec_size];
    load_t *values_vector = reinterpret_cast<load_t*>(values);

    while (idx * vec_size + vec_size - 1 < end) {
      *values_vector = reinterpret_cast<const load_t*>(data)[idx];
      #pragma unroll
      for (index_t i = 0; i < vec_size; i++) {
        value_list[i] = ops.reduce(value_list[i], values[i], shift + idx * vec_size + i);
      }
      idx += stride;
    }

    // tail
    index_t tail_start = end - end % vec_size;
    if (config.should_reduce_tail()) {
      int idx = tail_start + threadIdx.x;
      if (idx < end) {
        value_list[0] = ops.reduce(value_list[0], data[idx], idx + shift);
      }
    }

    // combine accumulators
    #pragma unroll
    for (int i = 1; i < vec_size; i++) {
      value_list[0] = ops.combine(value_list[0], value_list[i]);
    }
    return value_list[0];
  }

  template<typename offset_calc_t>
  C10_DEVICE arg_t thread_reduce_impl(const scalar_t* data, offset_calc_t calc) const {
    index_t idx = config.input_idx();
    const index_t end = config.num_inputs;
    const index_t stride = config.step_input;

    // Multiple accumulators to remove dependency between unrolled loops.
    arg_t value_list[vt0];
    #pragma unroll
    for (int i = 0; i < vt0; i++) {
      value_list[i] = ident;
    }

    scalar_t values[vt0];

    while (idx + (vt0 - 1) * stride < end) {
      #pragma unroll
      for (index_t i = 0; i < vt0; i++) {
        values[i] = data[calc(idx + i * stride)];
      }
      #pragma unroll
      for (index_t i = 0; i < vt0; i++) {
        value_list[i] = ops.reduce(value_list[i], values[i], idx + i * stride);
      }
      idx += stride * vt0;
    }

    // tail
    int idx_ = idx;
    #pragma unroll
    for (index_t i = 0; i < vt0; i++) {
      if (idx >= end) {
        break;
      }
      values[i] = data[calc(idx)];
      idx += stride;
    }
    idx = idx_;
    #pragma unroll
    for (index_t i = 0; i < vt0; i++) {
      if (idx >= end) {
        break;
      }
      value_list[i] = ops.reduce(value_list[i], values[i], idx);
      idx += stride;
    }

    // combine accumulators
    #pragma unroll
    for (int i = 1; i < vt0; i++) {
      value_list[0] = ops.combine(value_list[0], value_list[i]);
    }
    return value_list[0];
  }

  C10_DEVICE arg_t block_x_reduce(arg_t value, char* shared_memory) const {
    int dim_x = blockDim.x;
    arg_t* shared = (arg_t*)shared_memory;
    if (dim_x > warpSize) {
      int address_base = threadIdx.x + threadIdx.y*blockDim.x;
      shared[address_base] = value;
      for (int offset = dim_x/2; offset >= warpSize; offset >>= 1) {
        __syncthreads();
        if (threadIdx.x < offset && threadIdx.x + offset < blockDim.x) {
          arg_t other = shared[address_base + offset];
          value = ops.combine(value, other);
          shared[address_base] = value;
        }
      }
      dim_x = warpSize;
    }

    __syncthreads();

    for (int offset = 1; offset < dim_x; offset <<= 1) {
      arg_t other = ops.warp_shfl_down(value, offset);
      value = ops.combine(value, other);
    }
    return value;
  }

  C10_DEVICE arg_t block_y_reduce(arg_t value, char* shared_memory) const {
    arg_t* shared = (arg_t*)shared_memory;
    shared[config.shared_memory_offset(0)] = value;
    for (int offset = blockDim.y / 2; offset > 0; offset >>= 1) {
      __syncthreads();
      if (threadIdx.y < offset && threadIdx.y + offset < blockDim.y) {
        arg_t other = shared[config.shared_memory_offset(offset)];
        value = ops.combine(value, other);
        shared[config.shared_memory_offset(0)] = value;
      }
    }
    return value;
  }

  C10_DEVICE bool mark_block_finished() const {
    __shared__ bool is_last_block_done_shared;

    __syncthreads();
    if (threadIdx.x == 0 && threadIdx.y == 0) {
      int prev_blocks_finished = atomicAdd(&semaphores[blockIdx.x], 1);
      is_last_block_done_shared = (prev_blocks_finished == gridDim.y - 1);
    }

    __syncthreads();

    return is_last_block_done_shared;
  }

  template <bool can_acc>
  C10_DEVICE arg_t accumulate_in_output(
    out_scalar_t* out, arg_t value,
    typename std::enable_if<can_acc>::type* = nullptr
  ) const {
    return ops.combine(*out, value);
  }

  template <bool can_acc>
  C10_DEVICE out_scalar_t get_accumulated_output(
    out_scalar_t* out, arg_t value,
    typename std::enable_if<can_acc>::type* = nullptr
  ) const {
    assert(!final_output);
    return (out_scalar_t)value;
  }

  // This function should never be called --
  // it's the version of `accumulate_in_output`
  // when accumulation in the output is not possible.
  template <bool can_acc>
  C10_DEVICE arg_t accumulate_in_output(
    out_scalar_t*, arg_t,
    typename std::enable_if<!can_acc>::type* = nullptr
  ) const {
    assert(false); // can't use AT_ASSERT in Cuda.
    return arg_t {};
  }

  // This function should never be called --
  // it's the version of `get_accumulated_output`
  // when accumulation in the output is not possible.
  template <bool can_acc>
  C10_DEVICE out_scalar_t get_accumulated_output(
    out_scalar_t* out, arg_t value,
    typename std::enable_if<!can_acc>::type* = nullptr
  ) const {
    assert(false);
    return *out;
  }

  template<class T>
  C10_DEVICE void set_results(const T x, const index_t base_offset) const {
    assert(noutputs == 1);
    auto res = (out_scalar_t*)((char*)dst[0] + base_offset);
    *res = x;
  }

  //Currently implemented for max of two outputs
  template<class T>
  C10_DEVICE void set_results(const thrust::tuple<T, T> x, const index_t base_offset) const {
    if (noutputs >= 1) {
      auto res0 = (out_scalar_t*)((char*)dst[0] + base_offset);
      *res0 = thrust::get<0>(x);
    }
    if (noutputs >= 2) {
      auto res1 = (out_scalar_t *) ((char *) dst[1] + base_offset);
      *res1 = thrust::get<1>(x);
    }
  }

  C10_DEVICE void set_results_to_output(arg_t value, index_t base_offset) const {
    assert(final_output);
    set_results(ops.project(value), base_offset);
  }

  C10_DEVICE arg_t global_reduce(arg_t value, arg_t* acc, char* shared_memory) const {
    arg_t* reduce_buffer = (arg_t*)cta_buf;
    index_t output_idx = config.output_idx();
    auto base_offsets = output_calc.get(output_idx);
    auto out = (out_scalar_t*)((char*)dst[0] + base_offsets[0]);

    bool should_store = config.should_store(config.output_idx());
    if (should_store) {
      index_t offset = config.staging_memory_offset(blockIdx.y);
      reduce_buffer[offset] = value;
    }

    __threadfence(); // make sure writes are globally visible
    __syncthreads(); // if multiple warps in this block wrote to staging, make sure they're all done
    bool is_last_block_done = mark_block_finished();

    if (is_last_block_done) {
      value = ident;
      if (config.should_block_x_reduce()) {
        index_t input_offset = threadIdx.x + threadIdx.y * blockDim.x;
        index_t step = blockDim.x * blockDim.y;
        for (; input_offset < config.ctas_per_output; input_offset += step) {
          index_t idx = config.staging_memory_offset(input_offset);
          arg_t next = reduce_buffer[idx];
          value = ops.combine(value, next);
        }
      } else {
        index_t input_offset = threadIdx.y;
        index_t step = blockDim.y;
        for (; input_offset < config.ctas_per_output; input_offset += step) {
          index_t idx = config.staging_memory_offset(input_offset);
          arg_t next = reduce_buffer[idx];
          value = ops.combine(value, next);
        }
      }
      value = block_y_reduce(value, shared_memory);
      if (config.should_block_x_reduce()) {
        value = block_x_reduce(value, shared_memory);
      }
      if (should_store) {
        if (accumulate) {
          value = ops.translate_idx(value, base_idx);
        }

        if (acc == nullptr) {
          if (accumulate) {
            value = accumulate_in_output<can_accumulate_in_output>(out, value);
          }
          if (final_output) {
            set_results_to_output(value, base_offsets[0]);
          } else {
            *out = get_accumulated_output<can_accumulate_in_output>(out, value);
          }
        } else {
          if (accumulate) {
            value = ops.combine(*acc, value);
          }
          if (final_output) {
            set_results_to_output(value, base_offsets[0]);
          } else {
            *acc = value;
          }
        }
      }
    }

    return value;
  }
};

template<int nt, typename R>
static void launch_reduce_kernel(const ReduceConfig& config, const R& reduction) {
  dim3 block = config.block();
  dim3 grid = config.grid();

  auto stream = at::cuda::getCurrentCUDAStream();
  int shared_memory = config.shared_memory_size();
  reduce_kernel<nt, R><<<grid, block, shared_memory, stream>>>(reduction);
  AT_CUDA_CHECK(cudaGetLastError());
}

class AccumulationBuffer {
 public:
  AccumulationBuffer() {}

  AccumulationBuffer(size_t acc_t_size, size_t out_t_size, char* out_ptr, int64_t size) {
    out_ptr_ = (char*)out_ptr;
    if (out_t_size >= acc_t_size) {
      // reusing output buffer for accumulation.
      acc_ptr_ = (char*)out_ptr;
      numerator_ = 1;
      denominator_ = 1;
    } else {
      auto& allocator = *c10::cuda::CUDACachingAllocator::get();
      buffer_ = allocator.allocate(size);
      acc_ptr_ = (char*)buffer_.get();
      numerator_ = acc_t_size;
      denominator_ = out_t_size;
      reduce_fraction(numerator_, denominator_);
    }
  }

  char* get_acc_slice(char* out_ptr) {
    if (acc_ptr_ == nullptr) {
      return nullptr;
    }
    return acc_ptr_ + ((out_ptr - out_ptr_) * numerator_ / denominator_);
  }

 private:
  char* acc_ptr_ = nullptr;
  char* out_ptr_ = nullptr;
  size_t numerator_;
  size_t denominator_;
  at::DataPtr buffer_;
};

template <typename scalar_t, typename out_scalar_t, int vt0=4, typename ops_t, typename ident_t=double>
inline void gpu_reduce_kernel(TensorIterator& iter, const ops_t& ops, ident_t ident=0,
                              AccumulationBuffer* acc_buf_ptr=nullptr, int64_t base_idx=0) {
  AT_ASSERT(iter.numel() > 0 && iter.ntensors() - iter.noutputs() == 1 && iter.noutputs() >= 1);

  using traits = function_traits<decltype(&ops_t::reduce)>;
  using arg_t = typename traits::template arg<0>::type;
  static constexpr bool can_accumulate_in_output =
    std::is_convertible<arg_t, out_scalar_t>::value;

  bool can_use_32bit_indexing = iter.can_use_32bit_indexing();
  std::unique_ptr<AccumulationBuffer> owned_buf_ptr;

  // The acc_buf_ptr is a shared pointer. It is create at the first entrance and
  // reused by all recursive function calls.
  if (acc_buf_ptr == NULL) {
    // acc_buf_ptr holds buffer used for accumulation among multiple sub_iter
    // when accumulation in output is not possible.
    if (!can_accumulate_in_output && !can_use_32bit_indexing) {
      int64_t output_memory_size = 1;
      for (int dim = 0; dim < iter.ndim(); dim++) {
        output_memory_size = std::max(output_memory_size, iter.shape()[dim] * iter.strides(0)[dim]);
      }
      owned_buf_ptr.reset(new AccumulationBuffer(sizeof(arg_t),
                                                 sizeof(out_scalar_t),
                                                 (char*) iter.data_ptr(0),
                                                 output_memory_size * sizeof(arg_t)));
    } else {
      owned_buf_ptr.reset(new AccumulationBuffer());
    }
    acc_buf_ptr = owned_buf_ptr.get();
  }

  if (!can_use_32bit_indexing) {
    for (auto& sub_iter : iter.with_32bit_indexing()) {
      // Dim 0 is always the reduced dimension
      AT_ASSERT(sub_iter.strides(0)[0] == 0);
      int64_t sub_iter_base_idx = sub_iter.view_offsets()[0];

      gpu_reduce_kernel<scalar_t, out_scalar_t, vt0>(sub_iter, ops, ident,
          acc_buf_ptr, sub_iter_base_idx);
    }
    return;
  }

  const char* in_data = (char*)iter.data_ptr(iter.ntensors() - 1);
  char* out_data = (char*)iter.data_ptr(0);
  const auto noutputs = iter.noutputs();
  optional<char*> out_data_extra;
  if (noutputs > 1) {
    out_data_extra = (char*)iter.data_ptr(1);
  } else {
    out_data_extra = nullopt;
  }
  char* acc_data = acc_buf_ptr->get_acc_slice(out_data);

  // Start by assuming that each thread handles a single output and all
  // the inputs for that output.
  int64_t num_outputs = iter.num_output_elements();
  int64_t inputs_per_output = iter.numel() / num_outputs;
  int input_index = iter.ntensors() - 1;

  auto config = ReduceConfig(sizeof(arg_t), num_outputs, inputs_per_output);

  int64_t dim0;
  int64_t dim1;

  // Adjust block size to map block width to fastest changing dimension of input
  // tensor. This grants the best possible memory accessing pattern, given that
  // for non-contiguous tensor with space in between, we cannot have perfect
  // memory coalescing.
  int64_t fastest_moving_stride;
  bool reduction_on_fastest_striding_dimension =
      (iter.num_reduce_dims() == iter.ndim()) ||
      (iter.strides(/*arg=*/input_index)[0] <
       iter.strides(/*arg=*/input_index)[iter.num_reduce_dims()]);
  // Notice that dim0 & dim1 does NOT guarantee any launch configuration here!
  // dim0 & dim1 are more like the upper bound of the block dimension. The
  // actual launch config and reduction scheme is determined by setting values
  // to `config.input_mult` and `config.output_mult`.
  // We try to max out dim1 so that we have enough threads per CTA to deliver
  // performance for larger problem size.
  if (reduction_on_fastest_striding_dimension) {
    // Map block.x to the fastest reducing dimension. It implies:
    //   1. block_x_reduce is required.
    //   2. block.y now max out to num_outputs.
    dim0 = iter.shape()[0];
    dim1 = num_outputs;
    fastest_moving_stride = iter.strides(/*arg=*/input_index)[0];
  } else {
    // Map block.x to the fastest non reducing dimension. It implies:
    //   1. block_x_reduce is turned off.
    //   2. block.y now max out to inputs_per_output.
    dim0 = iter.shape()[iter.num_reduce_dims()];
    dim1 = inputs_per_output;
    fastest_moving_stride = iter.strides(/*arg=*/input_index)[iter.num_reduce_dims()];
  }

  // if the fastest moving dimension is contiguous and large enough, we do vectorized
  // load for better performance. Note that if vt0 < ReduceConfig::vec_size, then this
  // means the register pressure could be high, in such case, we should avoid vectorization.
  // We only vectorize 1D reduction
  if (fastest_moving_stride == sizeof(scalar_t) && dim0 > 128 && vt0 >= ReduceConfig::vec_size) {
    // TODO: vectorization on output is not supported yet
    if (reduction_on_fastest_striding_dimension && iter.num_reduce_dims() == 1) {
      config.vectorize = true;
    }
  }

  // Adjust block_width and block_height
  config.set_block_dimension(dim0, dim1);

  int block_width = config.block_width;
  int block_height = config.block_height;

  if (iter.ndim() == 0 || reduction_on_fastest_striding_dimension) {
    // Split the input across lanes if the input is contiguous in the reduced
    // dimension. This will require reduction between threads using warp
    // shuffle instructions and shared memory (if block_width > warpSize).
    config.input_mult[0] = config.split_input(block_width);
  } else {
    // Otherwise split the output across lanes in a warp.
    config.output_mult[0] = config.split_output(block_width);
  }

  if (config.values_per_thread() >= block_height * 16 || config.values_per_thread() >= 256) {
    // Divide the input across warps in a thread-block, if that leaves at least
    // 16 elements to be summed by each thread. This will require inter-warp
    // reduction using shared memory.
    config.input_mult[1] = config.split_input(block_height);
  } else {
    // Otherwise, each warp handles a separate output.
    config.output_mult[1] = config.split_output(block_height);
  }

  constexpr int min_values_per_thread = 16;
  constexpr int max_values_per_thread = 256;
  const int blocks_per_sm = at::cuda::getCurrentDeviceProperties()->maxThreadsPerMultiProcessor / (block_width * block_height);
  const int num_mp = at::cuda::getCurrentDeviceProperties()->multiProcessorCount;
  const int target_grid_size = num_mp * blocks_per_sm;
  int grid = config.grid().x;
  if (config.input_mult[1] != 0 && config.values_per_thread() >= max_values_per_thread && grid <= target_grid_size) {
    // Divide the input across thread-blocks if the amount of work per-thread
    // is large enough and the size of the output is small enough. This will
    // require a reduction using global memory.
    // If we decide to split input across blocks, as long as we can get enough
    // number of blocks (`target_grid_size`) to balance SM, we should still
    // make the number of values per thread large for best performance.
    int ctas_per_output1 = div_up(target_grid_size, grid);
    int ctas_per_output2 = div_up(config.values_per_thread(), min_values_per_thread);
    int ctas_per_output3 = div_up(config.values_per_thread(), max_values_per_thread);
    // We want the minimum of ctas_per_output1 and ctas_per_output2, so that each thread can have
    // a large number of values to deal with. But we don't want values_per_thread to be larger than
    // max_values_per_thread
    config.ctas_per_output = std::max(std::min<int>(ctas_per_output1, ctas_per_output2), ctas_per_output3);
    if (config.ctas_per_output > 1) {
      config.input_mult[2] = config.split_input(config.ctas_per_output);
    }
  }

  at::DataPtr buffer;
  at::DataPtr semaphores;
  if (config.should_global_reduce()) {
    auto& allocator = *c10::cuda::CUDACachingAllocator::get();
    buffer = allocator.allocate(config.global_memory_size());
    semaphores = allocator.allocate(config.semaphore_size());

    auto stream = at::cuda::getCurrentCUDAStream();
    AT_CUDA_CHECK(cudaMemsetAsync(semaphores.get(), 0, config.semaphore_size(), stream));
  }

  AT_ASSERT(can_use_32bit_indexing);
  auto output_calc = make_output_calculator<uint32_t>(iter);
  auto input_calc = make_input_calculator<uint32_t>(iter);
  auto reduce = ReduceOp<scalar_t, ops_t, uint32_t, out_scalar_t, vt0>(
      ops,
      config,
      input_calc,
      output_calc,
      in_data,
      out_data,
      out_data_extra,
      acc_data,
      buffer.get(),
      (int*)semaphores.get(),
      ident,
      noutputs,
      base_idx);
  reduce.accumulate = iter.should_accumulate();
  reduce.final_output = iter.is_final_output();

  launch_reduce_kernel<ReduceConfig::MAX_NUM_THREADS>(config, reduce);
}

}} // namespace at::native