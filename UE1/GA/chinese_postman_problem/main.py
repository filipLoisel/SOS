import numpy as np
from geneticalgorithm import geneticalgorithm as ga

from GA.chinese_postman_problem.fitness import fitness_function

var_boundaries = np.array([[0, 7]] * 21)
print(var_boundaries)

algorithm_param = {'max_num_iteration': 10000,
                   'population_size': 100,
                   'mutation_probability': 0.1,
                   'elit_ratio': 0,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type': 'uniform',
                   'max_iteration_without_improv': None}

model = ga(function=fitness_function,
           dimension=21,
           variable_type='int',
           variable_boundaries=var_boundaries,
           algorithm_parameters=algorithm_param)

model.run()
convergence = model.report
