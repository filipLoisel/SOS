graph = {
    'a': {1: 'b', 2: 'b'},
    'b': {3: 'c', 4: 'c'},
    'c': {7: 'a', 5: 'd'},
    'd': {6: 'c'}
}

edge_weights = {
    1: 4,
    2: 8,
    3: 5,
    4: 9,
    5: 3,
    6: 2,
    7: 6
}


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
    starting_point = 'a'
    current_vertex = starting_point
    distance = 0
    visited_edges = []
    for current_edge in data:
        edges = graph[current_vertex]

        if __has_traversed_full_graph(visited_edges, starting_point):
            return distance

        if current_edge not in edges:
            distance += 5000
        else:
            distance += edge_weights[current_edge]
            current_vertex = edges[current_edge]
            visited_edges.append(current_edge)

    return distance
