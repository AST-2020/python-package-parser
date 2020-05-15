from typing import List


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError(f"Parameter n must be non-negative (found n = {n})")

    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b

    return a


def factorial(n: int):
    if n < 0:
        raise ValueError(f"Parameter n must be non-negative (found n = {n})")

    result = 1
    for i in range(1, n + 1):
        result *= i

    print(result)


def collatz(n: int) -> List[int]:
    if n <= 0:
        raise ValueError(f"Parameter n must be positive (found n = {n})")

    result = [n]
    current = n
    while current != 1:
        following = current // 2 if current % 2 == 0 else 3 * current + 1

        result.append(following)
        current = following

    return result
