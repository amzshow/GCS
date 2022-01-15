"""
This module contains the class details for VM.
"""


__author__ = "Ahmad Awan"
__email__ = "i202004@nu.edu.pk"


class Vm():


	def __init__(self, id: int, mips: int):
		self.id = id
		self.mips = mips


	def get_id(self) -> int:
		return self.id


	def get_mips(self) -> int:
		return self.mips


	def __repr__(self):
		return f"VM {self.id}: {self.mips} MIPS"


	def __str__(self):
		return f"VM {self.id}: {self.mips} MIPS"
