import numpy as np
import pygad
import random
from math import inf

penalty = 1000000

L = 9
objects = [1,2,2,3,5,6,3,3,2]

objLen = len(objects)

def createInitSol(L, objects):


    patternList = []

    n = len(objects)

    currentStockUse = 0
    currentPattern = [0]*n

    for i in range(len(objects)):

        if currentStockUse + objects[i] < L:

            currentPattern[i] = objects[i]
            currentStockUse += objects[i]

        else:
            patternList.extend(currentPattern)
            currentPattern = [0]*n
            currentPattern[i] = objects[i]

    patternList.extend(currentPattern)


    return list(patternList)




def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]



#### PYGAD

def fitness_func(solution, solution_idx):
    score = 0



    for pattern in divide_chunks(solution, objLen):

        if sum(pattern) == 0:
            trimScore = 0
        else:

            trimScore = L - sum(pattern)

        if trimScore < 0:
            score -= penalty
        else:
            score -= trimScore
        

    return score






fitness_function = fitness_func

num_generations = 1000
num_parents_mating = 1

sol_per_pop = 100

initial_population = []


for i in range(sol_per_pop):
    initial_population.append(createInitSol(L, objects))



parent_selection_type = "sss"
keep_parents = 1

crossover_type = None

mutation_type = "swap"
mutation_percent_genes = 50

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       initial_population=initial_population,
                       sol_per_pop=sol_per_pop,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)


ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
