import numpy as np
import pygad
import random
from math import inf
import time
import pickle
import pandas as pd




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


#helper function to divide the solution into the pcutting patterns

def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]



#### PYGAD

# In the fitness function we calculate the trim score 
#and give penalties for trying to cut too much of the stock

def fitness_func(solution, solution_idx):
    score = 0

    #checking if all object are still included in the right quantity
    if sorted([int(i) for i in solution if i != 0]) != sorted(objects):
        score -= penalty*10


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




## Parameters ##

fitness_function = fitness_func

num_generations = 500
num_parents_mating = 10

sol_per_pop = 100

parent_selection_type = "sss"
keep_parents = 10

crossover_type = "single_point"

mutation_type = "swap"
mutation_percent_genes = 50

stop_criteria="saturate_50"

penalty = 1000000




pickle_in = open("csp_testset.pickle","rb")
test_set = pickle.load(pickle_in)

counter = 0
table_500 = [['n','Trimloss', 'runtime']]



for test in test_set['500'][1:3]:
    counter += 1
    print("Test {s} started".format(s=counter))
    starttime = time.time()


    initial_population = []


    for i in range(sol_per_pop):
        initial_population.append(createInitSol(test[0],test[1]))
    L = test[0]
    objects = test[1]
    objLen = len(test[1])

    ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       initial_population=initial_population,
                       sol_per_pop=sol_per_pop,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       stop_criteria=stop_criteria)

    ga_instance.run()


    endtime = time.time()
    runtime= endtime-starttime

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Test {s} complete".format(s=counter))
    print("Elapsed Time: {time}".format(time=runtime))

    table_500.append([500,solution_fitness,runtime])

pd.DataFrame(table_500).to_csv('ga_table_500.csv', header=False, index=False)