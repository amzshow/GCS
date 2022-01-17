"""
This module contains the class for genetic algorithm and its specification.
"""


__author__ = "Ahmad Awan"
__email__ = "i202004@nu.edu.pk"


import random
from typing import Tuple, List
from crossover import Crossover
from cloudlet import Cloudlet
from vm import Vm


class GeneticCloudScheduling():


	def __init__(self):
		# Number of Generations to iterate to
		self.N_GENERATIONS: int = 1
		# Desired Stopping condition based on fitness change ie DETLA FITNESS = NEW FITNESS - OLD FITNESS
		self.DESIRED_DELTA_FITNESS: float = 0
		# Number of generations for desired delta fitness to occur concurrently to stop
		self.DESIRED_DELTA_FITNESS_STAGNATION_N_GENERATION: int = 0
		# Number of VMs
		self.N_VMS: int = 1
		# Number of Cloudlets
		self.N_CLOUDLETS: int = 1
		# Total population size
		self.POPULATION_SIZE: int = 2
		# Size of tournament for tournament selection
		self.TOURNAMENT_SIZE: int = 2
		# Crossover type
		self.CROSSOVER: Crossover = Crossover.UNIFORM
		# Crossover rate
		self.CROSSOVER_RATE: float = 0.0
		# Mutation rate
		self.MUTATION_RATE: float = 0.0
		# Elitism rate
		self.ELITISM_RATE: float = 0.0
		# List of Individuals
		self.POPULATION: List[List[int]] = []
		# List of Cloudlets
		self.CLOUDLETS: List[Cloudlet] = []
		# List of VMs
		self.VMS: List[Vm] = []
		# List of selected inidividuals for crossover
		self.SELECTION: List[int] = []
		# List of Children
		self.CHILDREN: List[List[int]] = []
		# List of Inidividuals index saved due to elitism
		self.ELITISM: List[int] = []
		# POPULATION FITNESS
		self.FITNESS: List[int] = []


	def generate_vms(self, low: int, high: int) -> List[Vm]:
		"""
		Generate a list of VMs with the MIPS set as a random value between low and high ranges.
		
		:param low: MIPS lower range.
		:param high: MIPS higher range.

		:returns vms: List of VM.
		"""

		if low > high:
			low, high = high, low
		
		self.VMS = [Vm(i, random.randint(low, high)) for i in range(self.N_VMS)]
		return self.VMS


	def generate_cloudlets(self, low: int, high: int) -> List[Cloudlet]:
		"""
		Generate a list of cloudlets with the length set as a random value between low and high ranges.
		
		:param low: MIPS lower range.
		:param high: MIPS higher range.

		:returns cloudlets: List of tasks.
		"""

		if low > high:
			low, high = high, low

		self.CLOUDLETS = [Cloudlet(i, random.randint(low, high)) for i in range(self.N_CLOUDLETS)]

		return self.CLOUDLETS

	def generate_allele(self) -> int:
		"""
		Generate gene.
		This is the generates a random number between 0 and N_VMS - 1.

		:returns gene: gene
		"""

		return random.randint(0, self.N_VMS - 1)


	def generate_individual(self) -> List[int]:
		"""
		Generate an individual where the positions represent the ID of cloudlet while the value at each index represents which VM the cloudlet will be assigned to.
		For example, individual with chromosome [7, 11, 9] has three cloudlets where cloudlet #1, #2 and #3 are assigned to VM ID 7, 11 and 9 respectively.

		:returns inidividual: List of Integers
		"""

		return [self.generate_allele() for i in range(self.N_CLOUDLETS)]


	def generate_population(self) -> List[List[int]]:
		"""
		Generate the entire population of inidividuals.

		:returns population: List of individuals.
		"""

		self.POPULATION = [self.generate_individual() for j in range(self.POPULATION_SIZE)]
		return self.POPULATION


	def get_probability(self, probability: float) -> bool:
		"""
		Given the probability, return true or false of the event happening.

		:param probability: Between 0 and 1.

		:returns decisision: bool.
		"""

		return random.random() <= probability


	def produce_offspring(self, p1: List[int], p2: List[int]) -> Tuple[List[int], List[int]]:
		"""
		Produce two new offspring given parents P1 and P2.
		The crossover operation depends on CROSSOVER enum value.
		Current supported operations are uniform and single point crossover.

		:param p1: Parent p1.
		:param p2: Parent p2.

		:returns o1, o2: offspring 1 and offspring 2
		"""

		o1 = []
		o2 = []
		if self.CROSSOVER is Crossover.UNIFORM:
			for i in range(len(p1)):
				if self.get_probability(self.CROSSOVER_RATE):
					o1.append(p1[i])
					o2.append(p2[i])
				else:
					o1.append(p2[i])
					o2.append(p1[i])
		elif self.CROSSOVER is Crossover.SINGLE_POINT:
			point = random.randint(0, len(p1))
			o1 = p1[0:point] + p2[point:0]
			o1 = p2[0:point] + p1[point:0]
			
		return o1, o2


	def mutate(self, p1: List[int]):
		"""
		Apply mutation on individual with probability MUTATION_RATE.
		Every gene may be mutated for the provided individual p1.

		:param p1: Individual.

		:returns p1: Individual with mutated genes.
		"""

		for i in range(len(p1)):
			if self.get_probability(self.MUTATION_RATE):
				p1[i] = self.generate_allele()
		return p1
	

	def calculate_vm_completion_time(self, vm_id: int, p1: List[int]) -> float:
		"""
		Calculate completion time for a particular VM.

		:param vm_id: ID of VM.
		:param p1: Individual.

		:returns vm_ct: Completion time
		"""

		vm_ct:float = 0.0
		for i, _vm_id in enumerate(p1):
			if vm_id == _vm_id:
				vm_ct = vm_ct + (self.CLOUDLETS[i].get_length() / self.VMS[vm_id].get_mips())
		return vm_ct


	def calculate_all_vm_completion_time(self, p1: List[int]) -> List[float]:
		"""
		Calculate completion time for all VMs.

		:param p1: Individual.

		:returns vm_ct: Completion time of all VMs
		"""

		vm_ct = [0.0] * self.N_VMS

		for i, vm_id in enumerate(p1):
			vm_ct[vm_id] = vm_ct[vm_id] + (self.CLOUDLETS[i].get_length() / self.VMS[vm_id].get_mips())

		return vm_ct


	def calculate_fitness(self, p1: List[int]) -> float:
		"""
		Calculate fitness of an individual based on completion time.

		:param p1: Individual.

		:returns fitness: fitness value.
		"""

		fitness = 1 / max(self.calculate_all_vm_completion_time(p1))

		return fitness


	def calculate_fitness_all(self) -> List[float]:
		"""
		Calculate fitness of all inidividuals.

		:returns fitness: List of fitness values.
		"""

		self.FITNESS = [self.calculate_fitness(individual) for individual in self.POPULATION]

		# Sort population and fitness based on fitness
		local_fit = zip(self.FITNESS, self.POPULATION)
		local_fit = sorted(local_fit, key=lambda x : x[0], reverse=True)
		self.FITNESS, self.POPULATION = zip(*local_fit)

		return self.FITNESS


	def get_fitness_max(self) -> Tuple[float, List[int]]:
		"""
		Get the individual from population with maximum fitness.
		
		:returns (max_fitness, individual): Max fitness and the individual.
		"""

		max_f = max(self.FITNESS)
		max_p = self.POPULATION[self.FITNESS.index(max_f)]

		return max_f, max_p


	def elitism(self) -> List[int]:
		"""
		Perform Elitism based on ELITISM RATE.
		The fittest from the population will automatically preserved for the next generation.

		:returns elitism: List of individuals index by elitsm.
		"""

		if self.ELITISM_RATE:
			self.ELITISM = list(range(int(self.ELITISM_RATE * self.POPULATION_SIZE)))

		return self.ELITISM


	def selection(self) -> List[int]:
		"""
		Perform Tournament selection based on TOURNAMENT SIZE.
		Individuals based that were selected based on ELITISM will be excluded.

		:returns selection: List of selected individuals by index
		"""

		range_tournament = range(len(self.ELITISM), self.POPULATION_SIZE)
		self.SELECTION = []
 
		for _ in range(len(self.ELITISM), self.POPULATION_SIZE, 2):

			winner_a = None
			winner_b = None

			# While loop so same individual is not winner of both tournaments.
			while winner_a == winner_b:
				tournament_a = random.sample(range_tournament, self.TOURNAMENT_SIZE)
				tournament_b = random.sample(range_tournament, self.TOURNAMENT_SIZE)
				
				fitness_a = [self.FITNESS[x] for x in tournament_a]
				fitness_b = [self.FITNESS[x] for x in tournament_b]
				
				max_a = max(fitness_a)
				max_b = max(fitness_b)

				winner_a = tournament_a[fitness_a.index(max_a)]
				winner_b = tournament_b[fitness_b.index(max_b)]

			self.SELECTION.extend([winner_a, winner_b])

		return self.SELECTION


	def crossover(self) -> List[List[int]]:
		"""
		Perform crossover and store the children.
		The crossover operation depends on CROSSOVER enum value.

		:returns children: List of children.
		"""
		
		self.CHILDREN = []
		for i in range(0, len(self.SELECTION), 2):
			p1 = self.POPULATION[self.SELECTION[i]]
			p2 = self.POPULATION[self.SELECTION[i+1]]
			o1, o2 = self.produce_offspring(p1, p2)
			self.CHILDREN.extend([o1, o2])

		return self.CHILDREN

	
	def mutation(self) -> List[List[int]]:
		"""
		Perform mutation on the children given MUTATION RATE.A

		:returns children: List of children after mutation.
		"""

		for i, child in enumerate(self.CHILDREN):
			self.CHILDREN[i] = self.mutate(child)


	def next_generation(self) -> List[List[int]]:
		"""
		Select the next generation based on elitism and parent-child fitness.
		For next generations, the best two from the parent-child based on fitness will be saved.

		:returns population: List of individuals for the next generation.
		"""

		new_generation = [self.POPULATION[x] for x in self.ELITISM]

		for i in range(0, len(self.SELECTION), 2):

			p1, p2, o1, o2 = self.POPULATION[self.SELECTION[i]], self.POPULATION[self.SELECTION[i+1]], self.CHILDREN[i], self.CHILDREN[i+1]
			fp1, fp2, fo1, fo2 = self.FITNESS[self.SELECTION[i]], self.FITNESS[self.SELECTION[i+1]], self.calculate_fitness(o1), self.calculate_fitness(o2)

			ind = [p1, p2, o1, o2]
			fitness = [fp1, fp2, fo1, fo2]
			best = sorted(fitness, reverse=True)[:2]
			best_a = fitness.index(best[0])
			best_b = fitness.index(best[1])

			new_generation.extend([ind[best_a], ind[best_b]])
			
		self.POPULATION = new_generation

		return self.POPULATION


	def generate_syntethic_like_workload(self):
		"""
		Generate synthehic workload.
		Will overwrite N_CLOUDLETS and CLOUDLETS.
		Best to call this right before generate_population().
		"""

		counting = [20, 60, 5, 10, 5]
		amount = [(1, 250), (800, 1200), (1800, 2500), (7000, 10000), (30000, 45000)]
		self.N_CLOUDLETS = sum(counting)
		self.CLOUDLETS = []
		_id = 0

		for i, c in enumerate(counting):
			for j in range(c):
				self.CLOUDLETS.append(Cloudlet(_id, random.randint(*amount[i])))
				_id = _id + 1

	
	def generate_google_like_workload(self):
		"""
		Generate google workload.
		Will overwrite N_CLOUDLETS and CLOUDLETS.
		Best to call this right before generate_population().
		"""

		counting = [20, 40, 30, 4, 6]
		amount = [(15000, 55000), (59000, 90000), (101000, 135000), (150000, 337500), (525000, 900000)]
		self.N_CLOUDLETS = sum(counting)
		self.CLOUDLETS = []
		_id = 0

		for i, c in enumerate(counting):
			for j in range(c):
				self.CLOUDLETS.append(Cloudlet(_id, random.randint(*amount[i])))
				_id = _id + 1


	def random_results_ct(self) -> Tuple[List[int], List[float]]:
		"""
		Using random selection algorithm, generate the schedule and its completion time.

		:returns p1, vm_ct: Individual and its completion time.
		"""

		p1 = self.generate_individual()
		vm_ct = self.calculate_all_vm_completion_time(p1)

		return p1, vm_ct


	def round_robin_results_ct(self) -> Tuple[List[int], List[float]]:
		"""
		Using round robin algorithm, generate the schedule and its completion time.

		:returns p1, vm_ct: Individual and its completion time.
		"""

		p1 = []
		_x = 0
		for _ in range(self.N_CLOUDLETS):
			p1.append(_x)
			_x = (_x + 1) % self.N_VMS

		vm_ct = self.calculate_all_vm_completion_time(p1)

		return p1, vm_ct


	def mct_results_ct(self) -> Tuple[List[int], List[float]]:
		"""
		Using minimum completion time algorithm, generate the schedule and its completion time.

		:returns p1, vm_ct: Individual and its completion time.
		"""

		p1 = []
		vm_share = [0] * self.N_VMS

		for cl in self.CLOUDLETS:
			mn = min(vm_share)
			vm_id = vm_share.index(mn)
			vm_share[vm_id] = vm_share[vm_id] + (cl.get_length() / self.VMS[vm_id].get_mips())

			p1.append(vm_id)

		vm_ct = self.calculate_all_vm_completion_time(p1)

		return p1, vm_ct

	
	def minmin_results_ct(self) -> Tuple[List[int], List[float]]:
		"""
		Using min-min completion time algorithm, generate the schedule and its completion time.

		:returns p1, vm_ct: Individual and its completion time.
		"""
		
		p1 = []
		
		vm_share = [0] * self.N_VMS

		for i, cl in enumerate(self.CLOUDLETS):
			_vm_share = vm_share.copy()
			for j, vm in enumerate(self.VMS):
				_vm_share[j] = _vm_share[j] + (cl.get_length() / vm.get_mips())
			
			mn = min(_vm_share)
			vm_id = _vm_share.index(mn)

			vm_share[vm_id] = vm_share[vm_id] + (cl.get_length() / self.VMS[vm_id].get_mips())

			p1.append(vm_id)

		vm_ct = self.calculate_all_vm_completion_time(p1)

		return p1, vm_ct
