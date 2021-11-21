from ACO.chinese_postman_problem.data.generator import random_adjacency_matrix, matrix_to_dict

n = 5
amount_edges = (n * n - n) // 2
matrix = random_adjacency_matrix(n)
# matrix = [[0, 2, 4], [2, 0, 4], [4, 4, 0]]
print('matrix')
print(matrix)
print()
graph, edge_weights = matrix_to_dict(matrix)
# graph, edge_weights = {0: {1: 1, 2: 2}, 1: {1: 0, 3: 2}, 2: {2: 0, 3: 1}}, {1: 2, 2: 4, 3: 4}
print('graph')
print(graph)
print()
print('edge_weights')
print(edge_weights)
print('sum weights')
print(sum(list(edge_weights.values())))


def __has_traversed_full_graph(visited_edges, starting_point):
    current_vertex = starting_point

    if not all(item in visited_edges for item in edge_weights.keys()):
        return False

    for current_edge in visited_edges:
        edges = graph[current_vertex]
        if current_edge not in edges:
            return False

        current_vertex = edges[current_edge]

    return current_vertex == starting_point


def fitness_function(data):
    starting_point = 0
    current_vertex = starting_point
    distance = 0
    visited_edges = []
    for current_edge in data:
        edges = graph[current_vertex]

        if __has_traversed_full_graph(visited_edges, starting_point):
            if current_edge != 0:
                distance += 5000

        elif current_edge not in edges:
            distance += 500000
        else:
            distance += edge_weights[current_edge]
            current_vertex = edges[current_edge]
            visited_edges.append(current_edge)

    return distance
