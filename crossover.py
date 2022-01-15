"""
This module contains the enum for crossover type.
"""


__author__ = "Ahmad Awan"
__email__ = "i202004@nu.edu.pk"


from enum import Enum


class Crossover(Enum):
	UNIFORM = 0
	SINGLE_POINT = 1