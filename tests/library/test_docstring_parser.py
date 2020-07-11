import unittest
from unittest import TestCase
import library.parser._docstring_parser as dp


class Test(TestCase):
    def test__find_parameter_hint_string_epy_style(self):
        eingabe = """
         This is a javadoc style.

         @param param1: this is a first param
         @param param2: this is a second param
         @return: this is a description of what is returned
         @raise keyError: raises an exception
         """
        result = [('param1', 'this is a first param'), ('param2', 'this is a second param')]

        self.assertListEqual(result, dp._find_parameter_hint_string_epy_style(eingabe))

    def test__find_parameter_hint_string_google_style(self):
        input1 = """
        This is an example of Google style.
        
        Args:
            param1: This is a first param
            param2: This is a second param
        
        Returns:
            This is a description of what is returned.
        
        Raises:
            KeyError: Raises an exception.
        """
        output1 = [("param1", "", "This is a first param"), ("param2", "", "This is a second param")]
        self.assertListEqual(output1, dp._find_parameter_hint_string_google_style(input1))

        input2 = """
        Args:
        values(list of `numbers.Number` or `torch. * Tensor`):
        """
        output2 = [('values', 'list of `numbers.Number` or `torch. * Tensor`', '')]
        self.assertListEqual(output2, dp._find_parameter_hint_string_google_style(input2))

        input3 = """
        Args:
            value (Tensor):
        """
        output3 = [('value', 'Tensor', '')]
        self.assertListEqual(output3, dp._find_parameter_hint_string_google_style(input3))

        input4 = """
        Args:
        beta (Number, optional): multiplier for :attr:`mat` (:math:`\beta`)
        alpha (Number, optional): multiplier for :math:`mat1 @ mat2` (:math:`\alpha`)
        """
        output4 = [('beta', 'Number, optional', 'multiplier for :attr:`mat` (:math:`\beta`)'), ('alpha', 'Number, optional', 'multiplier for :math:`mat1 @ mat2` (:math:`\alpha`)')]
        self.assertListEqual(output4, dp._find_parameter_hint_string_google_style(input4))

        input5 = """
        Args:
            op_name: Check if this op is registered in `core._REGISTERED_OPERATORS`.
            message: message to fail with.
        
        Usage:
            @skipIfNotRegistered('MyOp', 'MyOp is not linked!')
                This will check if 'MyOp' is in the caffe2.python.core
        """
        output5 = [('op_name', '', 'Check if this op is registered in `core._REGISTERED_OPERATORS`.'), ('message', '', 'message to fail with.')]
        self.assertListEqual(output5, dp._find_parameter_hint_string_google_style(input5))

        input6 = """
        Args:
            model: input model
        
        Return:
            Quantized model.
        """
        output6 = [('model', '', 'input model')]
        self.assertListEqual(output6, dp._find_parameter_hint_string_google_style(input6))

        input7 = """
        Args:
            blob_name_tracker: Dictionary tracking names of blobs (inputs/outputs from operators)
        """
        output7 = [('blob_name_tracker', '', 'Dictionary tracking names of blobs (inputs/outputs from operators)')]
        self.assertListEqual(output7, dp._find_parameter_hint_string_google_style(input7))

        input8 = """
        Args:
            show_simplified: Whether to show a simplified version of the model graph
                Sets all of the following values:
                    clear_debug_info: Boolean representing whether to silence debug
                        info (which can be very verbose)
                    show_forward_only: Boolean representing whether to only show
                        blobs involved in the forward pass
                    show_cpu_only: Boolean representing whether to only show blobs
                        that are not associated with a gpu
                    use_tensorflow_naming: Boolean representing whether to convert
                        some common Caffe2 naming conventions to their Tensorflow
                        counterparts
        """
        """
        output8 = [('show_simplified', '', 'Whether to show a simplified version of the model graph\nSets all of the following values:
                            clear_debug_info: Boolean representing whether to silence debug
                                info (which can be very verbose)
                            show_forward_only: Boolean representing whether to only show
                                blobs involved in the forward pass
                            show_cpu_only: Boolean representing whether to only show blobs
                                that are not associated with a gpu
                            use_tensorflow_naming: Boolean representing whether to convert
                                some common Caffe2 naming conventions to their Tensorflow
                                counterparts')]
        """
        # self.assertListEqual(output8, dp._find_parameter_hint_string_google_style(input8))

    def test__find_parameter_hint_string_numpydoc_style(self):
        eingabe = """
        My numpydoc description of a kind
        of very exhautive numpydoc format docstring.

        Parameters
        ----------
        first : array_like
            the 1st param name `first`
        second :
            the 2nd param
        third : {'value', 'other'}, optional
            the 3rd param, by default 'value'

        Returns
        -------
        string
            a value in a string
        """

        result = [("first", "array_like"), ("second", ""), ("third", "{'value', 'other'}, optional")]

        self.assertListEqual(result, dp._find_parameter_hint_string_numpydoc_style(eingabe))

    def test__find_parameter_hint_string_rest_style(self):
        eingabe = """
        This is a reST style.
    
        :param param1: this is a first param
        :param param2: this is a second param
        :returns: this is a description of what is returned
        :raises keyError: raises an exception
        """

        result = [("param1", "this is a first param"), ("param2", "this is a second param")]

        self.assertListEqual(result, dp._find_parameter_hint_string_rest_style(eingabe))

    def test__find_hint_from_param_desc_rest_style(self):
        input1 = [('input', 'tensor of shape :math:`(N, C_{    ext{in}}, H, [W, D]))`')]
        output1 = {'input': ['tensor']}
        self.assertDictEqual(output1, dp._find_hint_from_param_desc_rest_style(input1))

        input2 = [('padding', '(tuple): m-elem tuple where m is the degree of convolution')]
        output2 = {'padding': ['tuple']}
        self.assertDictEqual(output2, dp._find_hint_from_param_desc_rest_style(input2))

        input3 = [('data', 'a list of values.')]
        output3 = {'data': ['list']}
        self.assertDictEqual(output3, dp._find_hint_from_param_desc_rest_style(input3))

        input4 = [('s', '(OPTIONAL) string.')]
        output4 = {'s': ['string']}
        self.assertDictEqual(output4, dp._find_hint_from_param_desc_rest_style(input4))

        input5 = [('s', 'a string object.')]
        output5 = {'s': ['string']}
        self.assertDictEqual(output5, dp._find_hint_from_param_desc_rest_style(input5))

        input6 = [('s', 'a normalized string.')]
        output6 = {'s': ['string']}
        self.assertDictEqual(output6, dp._find_hint_from_param_desc_rest_style(input6))

        input7 = [('type_', 'a string or a list of string.')]
        output7 = {'type_': ['string', 'list']}
        self.assertDictEqual(output7, dp._find_hint_from_param_desc_rest_style(input7))

        input8 = [('s', 'a string or file object with the ARFF file.')]
        output8 = {'s': ['string', 'file']}
        self.assertDictEqual(output8, dp._find_hint_from_param_desc_rest_style(input8))

        input9 = [('fp', 'a file-like object.')]
        output9 = {'fp': ['file-like']}
        self.assertDictEqual(output9, dp._find_hint_from_param_desc_rest_style(input9))

        input10 = [('encode_nominal', 'boolean, if True perform a label encoding')]
        output10 = {'encode_nominal': ['boolean']}
        self.assertDictEqual(output10, dp._find_hint_from_param_desc_rest_style(input10))

        input11 = [('obj', 'a dictionary.')]
        output11 = {'obj': ['dictionary']}
        self.assertDictEqual(output11, dp._find_hint_from_param_desc_rest_style(input11))

        input12 = [('obj', 'the object containing the ARFF information.')]
        output12 = {'obj': []}
        self.assertDictEqual(output12, dp._find_hint_from_param_desc_rest_style(input12))

    def test__find_hint_from_param_desc_google_style(self):
        input1 = [('value', '(Tensor)', 'A tensor of ``.dim()`` at least ``dim``.')]
        output1 = {'value': ['Tensor']}
        self.assertDictEqual(output1, dp._find_hint_from_param_desc_google_style(input1))

        input2 = [('mat1', '(SparseTensor)', 'the first sparse matrix to be multiplied')]
        output2 = {'mat1': ['SparseTensor']}
        self.assertDictEqual(output2, dp._find_hint_from_param_desc_google_style(input2))

        input3 = [('figure', '(matplotlib.pyplot.figure)', 'or list of figures or figure or a list of figures')]
        output3 = {'figure': ['matplotlib.pyplot.figure']}
        self.assertDictEqual(output3, dp._find_hint_from_param_desc_google_style(input3))

        input4 = [('name', '(str, optional)', 'name of weight parameter')]
        output4 = {'name': ['str']}
        self.assertDictEqual(output4, dp._find_hint_from_param_desc_google_style(input4))

        input5 = [('labels', '(torch.Tensor, numpy.array, or string/blobname)',
                   'Ground truth data. Binary label for each element.')]
        output5 = {'labels': ['torch.Tensor', 'numpy.array', 'string', 'blobname']}
        self.assertDictEqual(output5, dp._find_hint_from_param_desc_google_style(input5))

        input6 = [('model', '(cnn.CNNModelHelper, model_helper.ModelHelper)', 'The model to')]
        output6 = {'model': ['cnn.CNNModelHelper', 'model_helper.ModelHelper']}
        self.assertDictEqual(output6, dp._find_hint_from_param_desc_google_style(input6))

        input7 = [('size', '(int or Tuple[int, int] or Tuple[int, int, int])', 'output spatial')]
        output7 = {'size': ['int', 'Tuple[int, int]', 'Tuple[int, int, int]']}
        self.assertDictEqual(output7, dp._find_hint_from_param_desc_google_style(input7))

        input8 = [('constraint', '(subclass of :class:`~torch.distributions.constraints.Constraint`)',
                   'A subclass of :class:`~torch.distributions.constraints.Constraint`, or')]
        output8 = {'constraint': ['subclass']}  # <- subclass should be ignored
        self.assertDictEqual(output8, dp._find_hint_from_param_desc_google_style(input8))

        input9 = [('method', '', 'the method (for example, Class.method)')]
        self.assertIsNone(dp._find_hint_from_param_desc_google_style(input9))
        # returns None at the moment

    def test__find_hint_from_param_desc_numpydoc_style(self):
        input1 = [('order', "'F', 'C' or None, default=None")]
        output1 = {'order': ['None', 'str']}
        self.assertDictEqual(output1, dp._find_hint_from_param_desc_numpydoc_style(input1))

        input2 = [('relevant_args', 'iterable of array-like')]
        output2 = {'relevant_args': ['iterable']}
        self.assertDictEqual(output2, dp._find_hint_from_param_desc_numpydoc_style(input2))

        input3 = [('X', '(sparse) array-like of shape (n_samples, n_features)')]
        output3 = {'X': ['array-like']}
        # self.assertDictEqual(output3, dp._find_hint_from_param_desc_numpydoc_style(input3))

        input4 = [('n_samples', 'int greater than 0,')]
        output4 = {'n_samples': ['int']}
        self.assertDictEqual(output4, dp._find_hint_from_param_desc_numpydoc_style(input4))

        input5 = [('eps', 'float in ]0,1[, optional (default=0.1)')]
        output5 = {'eps': ['float']}
        self.assertDictEqual(output5, dp._find_hint_from_param_desc_numpydoc_style(input5))

        input6 = [('n_components', 'int,')]
        output6 = {'n_components': ['int']}
        self.assertDictEqual(output6, dp._find_hint_from_param_desc_numpydoc_style(input6))

        input7 = [('.. versionadded', ': 0.17')]
        self.assertIsNone(dp._find_hint_from_param_desc_numpydoc_style(input7))

        input8 = [('multioutput', "string in ['raw_values', 'uniform_average'] or array-like of shape (n_outputs)")]
        output8 = {'multioutput': ['array-like', 'string']}
        self.assertDictEqual(output8, dp._find_hint_from_param_desc_numpydoc_style(input8))

        input9 = [('.. deprecated', ': 0.22')]
        output9 = {'.. deprecated': [': 0.22']}
        self.assertIsNone(dp._find_hint_from_param_desc_numpydoc_style(input9))

        input10 = [('subset', "'train' or 'test', 'all', optional")]
        output10 = {'subset': ['str']}
        self.assertDictEqual(output10, dp._find_hint_from_param_desc_numpydoc_style(input10))

        input11 = [('grads', 'list, length = len(params)')]
        output11 = {'grads': ['list']}
        self.assertDictEqual(output11, dp._find_hint_from_param_desc_numpydoc_style(input11))
        # do not know how to differentiate from hint separator except comparing for length

        input12 = [('X',
                    'BallTree, KDTree or {array-like, sparse matrix} of shape (n_samples, n_features) or (n_samples, n_samples)')]
        output12 = {'X': ['BallTree', 'KDTree', 'array-like', 'sparse matrix']}
        self.assertDictEqual(output12, dp._find_hint_from_param_desc_numpydoc_style(input12))

    def test__find_parameter_hint_in_doc_string(self):
        doc_string = """Splits the tensor into chunks. Each chunk is a view of the original tensor.

            If :attr:`split_size_or_sections` is an integer type, then :attr:`tensor` will
            be split into equally sized chunks (if possible). Last chunk will be smaller if
            the tensor size along the given dimension :attr:`dim` is not divisible by
            :attr:`split_size`.

            If :attr:`split_size_or_sections` is a list, then :attr:`tensor` will be split
            into ``len(split_size_or_sections)`` chunks with sizes in :attr:`dim` according
            to :attr:`split_size_or_sections`.

            Arguments:
                tensor (Tensor): tensor to split.
                split_size_or_sections (int) or (list(int)): size of a single chunk or
                    list of sizes for each chunk
                dim (int): dimension along which to split the tensor.
            """
        from library.convert_string_to_type import convert_string_to_type

        print(convert_string_to_type('list[Tensor]'))

        print (dp._find_parameter_hint_in_doc_string(['tensor', 'split_size_or_sections', 'dim'], doc_string))

if __name__ == '__main__':
    unittest.main()
