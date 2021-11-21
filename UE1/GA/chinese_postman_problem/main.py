import timeit

import numpy as np
from geneticalgorithm import geneticalgorithm as ga

from GA.chinese_postman_problem.fitness import fitness_function

n = 5
amount_edges = (n * n - n) // 2
var_boundaries = np.array([[0, n + 1]] * amount_edges * 4)

algorithm_param = {'max_num_iteration': 1000,
                   'population_size': 100,
                   'mutation_probability': 0.1,
                   'elit_ratio': 0.01,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type': 'uniform',
                   'max_iteration_without_improv': None}

start = timeit.default_timer()

model = ga(function=fitness_function,
           dimension=amount_edges * 4,
           variable_type='int',
           variable_boundaries=var_boundaries,
           algorithm_parameters=algorithm_param)

model.run()
stop = timeit.default_timer()
print('Time: ', stop - start)
convergence = model.report
