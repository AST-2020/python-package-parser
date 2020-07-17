from experiments.star_import_problems.package.scalar import add as scalar_add
from experiments.star_import_problems.package.vec import add as vec_add
import random


add = scalar_add if random.random() < 0.5 else vec_add

__all__ = ["add"]
