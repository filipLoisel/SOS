import numpy as np
from copy import copy
import random
import time
import math
import pickle
import pandas as pd

## pheromone matrix ##

#length of the stock
L = 50

#objects to cut

objects = [random.randint(2, L-int(L/2)) for i in range(200)]

def ACO(L,objects):

	#parameters

	generations = 100

	stop_criteria = 3

	nants = 5 #len(objects)

	beta = 2 # 2, 5 or 10.

	rho = 0.95# pheromone evaporation

	gamma = 500/len(objects) # global best ant or run best ant

	# create initial values for pheromone matrix
	pheromone_matrix = np.random.rand(L,L)/5#np.zeros((L, L)) + 1/1-rho

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

	def pheromone_randomizer():
		for i in range(L):
			for j in range(L):
				pheromone_matrix[i,j] = pheromone_matrix[i,j]*random.uniform(0,1)

	## fitness function ## 

	def fitness(solution):

		#return 1/(0.0001+trim_loss(solution))

		return sum([sum(pattern)/L for pattern in solution])**2/len(solution)

	def trim_loss(solution):
		score = 0
		for pattern in solution:
			if sum(pattern) == 0:
				trimScore = 0
			else:
				trimScore = L - sum(pattern)
			score += trimScore
		return score


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

					if space_left < item:
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

	same_sbest = 0

	global_best_fitness = 0
	global_best_solution = None

	for gen in range(generations):

		if same_sbest >= stop_criteria:
			print("No progress: stopping")
			break

		#print("\ncalculating gen: " + str(gen))
		#print(pheromone_matrix)

		# calculate current generation of solutions

		gen_solutions = calc_generation()

		#find best solution based on fitness

		gen_fitness = [fitness(x) for x in gen_solutions]
		best_fitness = max(gen_fitness)

		if best_fitness > global_best_fitness:
			global_best_fitness = best_fitness
			global_best_solution = gen_solutions[gen_fitness.index(best_fitness)]

		else:
			same_sbest += 1
		
		sbest = gen_solutions[gen_fitness.index(best_fitness)]



		#save best solution for each generation

		global_best_sols.append([sbest, fitness(sbest), trim_loss(sbest)])


		#update based on best solution

		#print(fitness(sbest))
		#print(trim_loss(sbest))

		update(sbest)

		#pheromone_randomizer()

		#pheromone_matrix = pheromone_matrix/np.max(pheromone_matrix)


	return(global_best_sols, [global_best_solution, global_best_fitness, trim_loss(global_best_solution)])



pickle_in = open("csp_testset.pickle","rb")
test_set = pickle.load(pickle_in)

counter = 0
table_500 = [['n','Trimloss', 'Fitness', 'runtime']]
for test in test_set['500'][1:3]:
	counter += 1
	print("Test {s} started".format(s=counter))
	starttime = time.time()
	result = ACO(test[0],test[1])
	endtime = time.time()
	runtime= endtime-starttime
	print("Test {s} complete".format(s=counter))
	print("Elapsed Time: {time}".format(time=runtime))

	table_500.append([500,result[-1][-1],result[-1][-2],runtime])

pd.DataFrame(table_500).to_csv('aco_table_500.csv', header=False, index=False)

