import random


def a():
    return 1


def b():
    return 2


exported = "a" if random.random() < 0.5 else "b"

__all__ = [exported]
