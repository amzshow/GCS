"""
This module contains the code for running the genetic algorithm and comparison with other algorithms
"""


__author__ = "Ahmad Awan"
__email__ = "i202004@nu.edu.pk"


from gcs import GeneticCloudScheduling
from crossover import Crossover
from datatype import DataType


if __name__ == '__main__':

	gcs = GeneticCloudScheduling()
	
	# Set parameters
	gcs.N_GENERATIONS = 1000
	gcs.N_VMS = 20
	gcs.POPULATION_SIZE = 100
	gcs.CROSSOVER = Crossover.UNIFORM # Use UNIFORM or SINGLE_POINT
	gcs.CROSSOVER_RATE = 0.10
	gcs.MUTATION_RATE = 0.01
	gcs.ELITISM_RATE = 0.02
	gcs.DESIRED_DELTA_FITNESS = 0
	gcs.DESIRED_DELTA_FITNESS_STAGNATION_N_GENERATION = 7
	data_type = DataType.GOOGLE # Use TESTING, GOOGLE or SYNTETHIC

	# Change datatype between TESTING, GOOGLE and SYNTETHIC for different workload. 
	# TESTING WORKLOAD is bad for simulation as workload is too small and too randomized.
	# Better to use GOOGLE or SYNTETHIC workload which can be commented or uncommented out below.
	
	if data_type is DataType.TESTING:

		print("USING TESTING WORKLOAD")
		gcs.N_CLOUDLETS = 100
		gcs.generate_cloudlets(400, 1000)

	elif data_type is DataType.GOOGLE:

		print("USING GOOGLE LIKE WORKLOAD")
		gcs.generate_google_like_workload()

	elif data_type is DataType.SYNTETHIC:

		print("USING SYNTHETIC WORKLOAD")
		gcs.generate_syntethic_like_workload()

	# Generate population and VMs
	gcs.generate_population()
	gcs.generate_vms(250, 2000)

	print(f"Starting Genetic algorithm for {gcs.N_GENERATIONS} generations optimizing for {gcs.N_VMS} VMs")

	# Initialize Additional Data
	fitness_track = []
	delta_fitness_track = []
	generation = 0
	fitness = 0
	old_fitness = 0

	# Main loop
	while generation < gcs.N_GENERATIONS:

		gcs.calculate_fitness_all()

		# Calculate fitness deltas and store them for historical data
		old_fitness = fitness
		fitness, fittest_individual = gcs.get_fitness_max()
		delta_fitness = fitness - old_fitness
		fitness_track.append(fitness)
		delta_fitness_track.append(delta_fitness)

		print(f"Generations:\t{generation + 1} / {gcs.N_GENERATIONS}\t| Δ {delta_fitness}\t| ΣΔ {sum(delta_fitness_track[-3:])}")

		# If max and min of delta fitness for x generations is equal to or below DESIRED DELTA FITNESS for DESIRED_DELTA_FITNESS_STAGNATION_N_GENERATION generations, stop
		if len(delta_fitness_track) >= gcs.DESIRED_DELTA_FITNESS_STAGNATION_N_GENERATION \
			and min(delta_fitness_track[-gcs.DESIRED_DELTA_FITNESS_STAGNATION_N_GENERATION:]) <= gcs.DESIRED_DELTA_FITNESS \
			and max(delta_fitness_track[-gcs.DESIRED_DELTA_FITNESS_STAGNATION_N_GENERATION:]) <= gcs.DESIRED_DELTA_FITNESS:
			break

		# Perform Genetic Operations
		gcs.elitism()
		gcs.selection()
		gcs.crossover()
		gcs.mutation()

		gcs.next_generation()

		generation = generation + 1

	# Get final fitness
	gcs.calculate_fitness_all()
	fitness, fittest_individual = gcs.get_fitness_max()
	fitness_track.append(fitness)

	ind_vm_ct = gcs.calculate_all_vm_completion_time(fittest_individual)
	sct = max(ind_vm_ct)
	fct = min(x for x in ind_vm_ct if x > 0)
	act = sum(ind_vm_ct) / len(ind_vm_ct)

	print("\n==============================================\n")

	print("FINAL RESULTS")
	print(f"FINAL GENERATION: {generation + 1} / {gcs.N_GENERATIONS}")
	print(f"BEST FITNESS: {fitness}")
	if gcs.N_CLOUDLETS <= 20:
		print(f"FITTEST INDIVIDUAL CHROMOSOME: {fittest_individual}")
	if gcs.N_VMS <= 20:
		print(f"FITTEST INDIVIDUAL COMPLETION TIME FOR EACH VM IN SECONDS {ind_vm_ct}")
	print(f"FITNESS HISTORY {fitness_track}")
	print(f"FITTEST INDIVIDUAL SLOWEST COMPLETION TIME: {sct}")
	print(f"FITTEST INDIVIDUAL FASTEST COMPLETION TIME: {fct}")
	print(f"FITTEST INDIVIDUAL AVERAGE COMPLETION TIME: {act}")

	print("\n==============================================\n")
	
	print("\nComparison with other algorithms")

	print("\nRandom Selection (RS) Algorithm")

	rp1, rind_vm_ct = gcs.random_results_ct()
	rsct = max(rind_vm_ct)
	rfct = min(x for x in rind_vm_ct if x > 0)
	ract = sum(rind_vm_ct) / len(rind_vm_ct)

	print(f"FITTEST INDIVIDUAL SLOWEST COMPLETION TIME: {rsct}")
	print(f"FITTEST INDIVIDUAL FASTEST COMPLETION TIME: {rfct}")
	print(f"FITTEST INDIVIDUAL AVERAGE COMPLETION TIME: {ract}")

	print("\nRound Robin (RR) Algorithm")

	rrp1, rrind_vm_ct = gcs.round_robin_results_ct()
	rrsct = max(rrind_vm_ct)
	rrfct = min(x for x in rrind_vm_ct if x > 0)
	rract = sum(rrind_vm_ct) / len(rrind_vm_ct)

	print(f"FITTEST INDIVIDUAL SLOWEST COMPLETION TIME: {rrsct}")
	print(f"FITTEST INDIVIDUAL FASTEST COMPLETION TIME: {rrfct}")
	print(f"FITTEST INDIVIDUAL AVERAGE COMPLETION TIME: {rract}")

	print("\nMinumum Completion Time (MCT) Algorithm")

	mp1, mind_vm_ct = gcs.mct_results_ct()
	msct = max(mind_vm_ct)
	mfct = min(x for x in mind_vm_ct if x > 0)
	mact = sum(mind_vm_ct) / len(mind_vm_ct)
	
	print(f"FITTEST INDIVIDUAL SLOWEST COMPLETION TIME: {msct}")
	print(f"FITTEST INDIVIDUAL FASTEST COMPLETION TIME: {mfct}")
	print(f"FITTEST INDIVIDUAL AVERAGE COMPLETION TIME: {mact}")

	print("\nMin-Min Algorithm")

	mmnp1, mmnind_vm_ct = gcs.minmin_results_ct()
	mmnsct = max(mmnind_vm_ct)
	mmnfct = min(x for x in mmnind_vm_ct if x > 0)
	mmnact = sum(mmnind_vm_ct) / len(mmnind_vm_ct)
	
	print(f"FITTEST INDIVIDUAL SLOWEST COMPLETION TIME: {mmnsct}")
	print(f"FITTEST INDIVIDUAL FASTEST COMPLETION TIME: {mmnfct}")
	print(f"FITTEST INDIVIDUAL AVERAGE COMPLETION TIME: {mmnact}")

	print("\n==============================================\n")

	print("\nRatio of Genetic Algorithm to other algorithms. Generally, less than 1 means Genetic Algorithm is better, greater than 1 means other algorithm performed better while equal to 1 means that there is no benefit for choosing one or the other.\n")

	print(f"GCS-RS SLOWEST COMPLETION TIME RATIO: {sct / rsct}")
	print(f"GCS-RR SLOWEST COMPLETION TIME RATIO: {sct / rrsct}")
	print(f"GCS-MCT SLOWEST COMPLETION TIME RATIO: {sct / msct}")
	print(f"GCS-Min-MIN SLOWEST COMPLETION TIME RATIO: {sct / mmnsct}")

	print("")

	print(f"GCS-RS FASTEST COMPLETION TIME RATIO: {fct / rfct}")
	print(f"GCS-RR FASTEST COMPLETION TIME RATIO: {fct / rrfct}")
	print(f"GCS-MCT FASTEST COMPLETION TIME RATIO: {fct / mfct}")
	print(f"GCS-Min-MIN FASTEST COMPLETION TIME RATIO: {fct / mmnfct}")

	print("")

	print(f"GCS-RS AVERAGE COMPLETION TIME RATIO: {act / ract}")
	print(f"GCS-RR AVERAGE COMPLETION TIME RATIO: {act / rract}")
	print(f"GCS-MCT AVERAGE COMPLETION TIME RATIO: {act / mact}")
	print(f"GCS-Min-MIN AVERAGE COMPLETION TIME RATIO: {act / mmnact}")

	print("\n==============================================\n")

	print("\nNote: Fastest Completion time is not the best metric, Slowest and Average Completion time are much better metrics for comparison.")
	print("This is because the longer a virtual machines runs, it will consume more power, resulting in higher usage cost, billing and CO2 emmissions.")
	print("Fastest Completion Time represents which VM will finish first and time taken.")
	print("Slowest Completion Time represents which VM will finish last and time taken.")
	print("Average Completion Time represents the average time each VM is taking to finish.")