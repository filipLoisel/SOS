import random

import numpy as np


def edge_name_matrix(n, vals):
    m = np.zeros([n, n], dtype=np.int)
    xs, ys = np.triu_indices(n, k=1)
    m[xs, ys] = vals
    m[ys, xs] = vals
    m[np.diag_indices(n)] = 0
    return m


def random_adjacency_matrix(n):
    matrix = [[random.randint(1, 7) for i in range(n)] for j in range(n)]

    # No vertex connects to itself
    for i in range(n):
        matrix[i][i] = 0

    # If i is connected to j, j is connected to i
    for i in range(n):
        for j in range(n):
            matrix[j][i] = matrix[i][j]

    return matrix


def matrix_to_dict(matrix):
    n = len(matrix)
    amount_edges = (n * n - n) // 2
    edge_names = edge_name_matrix(n, list(range(1, amount_edges + 1)))
    graph = {}
    edge_weights = {}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            weight = matrix[i][j]
            edge_name = edge_names[i][j]
            edge_weights[edge_name] = weight

            connections = graph.get(i, {})
            connections[edge_name] = j
            graph[i] = connections

    return graph, edge_weights
