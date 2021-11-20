import numpy as np

## pheromone matrix ##

#length of the stock
L = 4
#objects to cut
objects = [1,2,2,3,2]

pheromone_matrix = np.zeros((L, L))





## heuristic ##

 # η(j) = j

 #parameters

nants = len(objects)

beta = 5 # 2, 5 or 10.

rho = 0.95# pheromone evaporation

gamma = 500/len(objects) # global best ant or run best ant

# create initial values for pheromone matrix


phermone_matrix = pheromone_matrix + 1/1-rho

## solution ##

def check_item(current_pattern, item, items_left):
	# calculates the probability to cut an item from the stock based on the pheromone matirix and the heuristik
	pattern_len = len(current_pattern)

	def calc_pheromone_value(current_pattern, j):
		if pattern_len > 0:
			return sum([pheromone_matrix[i,j] for i in current_pattern])/pattern_len
		else:
			return 1

	if (item in items_left):

		prob = (calc_pheromone_value(current_pattern, item)*(item**beta))/sum([calc_pheromone_value(current_pattern, g)*(g**beta) for g in items_left])
	
	else:
		return 0


## update pheromone trail ##

# τ(i,j) = ρ.τ(i,j) + m.f(sbest) 

pheromone_matrix[i,j] = rho*pheromone_matrix[i,j]

## fittness function ## 