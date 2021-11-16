import numpy as np
from geneticalgorithm import geneticalgorithm as ga


# library tries to minimize f
def fitness_function(data):
    return np.sum(data)


varbound = np.array([[1, 10]] * 3)
print(varbound)

algorithm_param = {'max_num_iteration': 3000,
                   'population_size': 100,
                   'mutation_probability': 0.1,
                   'elit_ratio': 0,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type': 'uniform',
                   'max_iteration_without_improv': None}

model = ga(function=fitness_function,
           dimension=3,
           variable_type='int',
           variable_boundaries=varbound,
           algorithm_parameters=algorithm_param)

model.run()
convergence = model.report
