"""
This module contains the class details for Cloudlet.
"""


__author__ = "Ahmad Awan"
__email__ = "i202004@nu.edu.pk"


class Cloudlet():
	

	def __init__(self, id: int, length: int):
		self.id = id
		self.length = length

	
	def get_id(self) -> int:
		return self.id
	

	def get_length(self) -> int:
		return self.length


	def __repr__(self):
		return f"Cloudlet {self.id}: {self.length} MI"


	def __str__(self):
		return f"Cloudlet {self.id}: {self.length} MI"
