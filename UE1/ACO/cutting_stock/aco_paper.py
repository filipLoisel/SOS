import numpy as np
from copy import copy
import random

## pheromone matrix ##

#length of the stock
L = 234

#objects to cut
#objects = [4,4,5,5,5,6,7,7,8,8,8,8,8,8,5,2,3,4,5]
objects = [random.randint(2, L-1) for i in range(50)]

def ACO(L,objects):

	#parameters

	generations = 10

	nants = len(objects)

	beta = 2 # 2, 5 or 10.

	rho = 0.95# pheromone evaporation

	gamma = 500/len(objects) # global best ant or run best ant

	# create initial values for pheromone matrix
	pheromone_matrix = np.zeros((L, L)) + 1/1-rho

	## solution ##

	def check_item(current_pattern, item, items_left):
		# calculates the probability to cut an item from the stock based on the pheromone matirix and the heuristik
		
		def calc_pheromone_value(current_pattern, j):
			pattern_len = len(current_pattern)

			if pattern_len > 0:
				return sum([pheromone_matrix[i,j] for i in current_pattern])/pattern_len
			else:
				return 1

		if (item in items_left):

			return (calc_pheromone_value(current_pattern, item)*(item**beta))/sum([calc_pheromone_value(current_pattern, g)*(g**beta) for g in items_left])
		
		else:

			return 0


	## update pheromone trail ##

	# τ(i,j) = ρ.τ(i,j) + m.f(sbest) 

	def update(sbest):
		for i in range(L):
			for j in range(L):
				m = 0
				for pattern in sbest:
					count_i = pattern.count(i)
					count_j = pattern.count(j)

					if (count_i != 0) and (count_j != 0):
						m += i*j
				pheromone_matrix[i,j] = rho*pheromone_matrix[i,j] + m*fitness(sbest)

	## fitness function ## 

	def fitness(solution):

			return sum([sum(pattern)/L for pattern in solution])**2/len(solution)

	## calculate one generation ##

	def calc_generation():
		solutions = []


		for ant in range(nants):


			solution = []
			current_pattern = []
			unassigned_items = copy(objects)
			items_left_to_check = copy(objects)

			while len(unassigned_items) > 0:


				choice_prob = []
				for item in unassigned_items:

					space_left = L - sum(current_pattern)

					if L - sum(current_pattern) < item:
						choice_prob.append(0)
					else:
						items_left_to_check = [x for x in items_left_to_check if x <= space_left] 
						choice_prob.append(check_item(current_pattern, item, items_left_to_check))

				if sum(choice_prob) == 0:

					#if pattern is full start new pattern

					solution.append(current_pattern)
					current_pattern = []
					items_left_to_check = copy(unassigned_items)


				else:

					#adding item with the highest probability to the current patter
					best_choice = unassigned_items[choice_prob.index(max(choice_prob))]
					current_pattern.append(best_choice)
					unassigned_items.remove(best_choice)

			solutions.append(solution)

		return solutions

	## main loop ##

	global_best_sols = []

	for gen in range(generations):


		print("\ncalculating gen: " + str(gen))

		# calculate current generation of solutions

		gen_solutions = calc_generation()

		#find best solution based on fitness

		gen_fitness = [fitness(x) for x in gen_solutions]
		sbest = gen_solutions[gen_fitness.index(max(gen_fitness))]

		#save best solution for each generation

		global_best_sols.append([sbest, fitness(sbest)])


		#update based on best solution

		print(fitness(sbest))

		update(sbest)


	return(global_best_sols)

print(ACO(L,objects))