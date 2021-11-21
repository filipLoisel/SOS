import timeit

from ACO.chinese_postman_problem.data.generator import random_adjacency_matrix, matrix_to_dict
from ACO.chinese_postman_problem.library import ACS_Ant, Solve


class CPPInstance:
    def __init__(self, n):
        self.starting_point = 1

        matrix = random_adjacency_matrix(n)
        #matrix = [[0, 7, 3, 1, 4], [7, 0, 5, 5, 3], [3, 5, 0, 5, 4], [1, 5, 5, 0, 1], [4, 3, 4, 1, 0]]
        print('matrix')
        print(matrix)
        print()
        self.graph, self.edge_weights = matrix_to_dict(matrix)
        #self.graph, self.edge_weights = {0: {1: 1, 2: 2, 3: 3, 4: 4}, 1: {1: 0, 5: 2, 6: 3, 7: 4}, 2: {2: 0, 5: 1, 8: 3, 9: 4}, 3: {3: 0, 6: 1, 8: 2, 10: 4}, 4: {4: 0, 7: 1, 9: 2, 10: 3}} ,{1: 7, 2: 3, 3: 1, 4: 4, 5: 5, 6: 5, 7: 3, 8: 5, 9: 4, 10: 1}
        print('graph')
        print(self.graph)
        print()
        print('edge_weights')
        print(self.edge_weights)
        print('sum weights')
        print(sum(list(self.edge_weights.values())))

    def getWeight(self, edge):
        return self.edge_weights[edge]

    def getEdges(self):
        return self.edge_weights.keys()

    def getPossbileNextEdgesByVertex(self, vertex):
        return self.graph[vertex]

    def getStartPoint(self):
        return self.starting_point

    def getGraph(self):
        return self.graph

    def getNextVertex(self, current_vertex, next_edge):
        return self.graph[current_vertex][next_edge]


class CPPAnt(ACS_Ant):
    def __init__(self, instance, **kwargs):
        self.instance = instance

        super().__init__(**kwargs)

    def getComponentCost(self, component):
        return self.instance.getWeight(*[component])

    def __has_traversed_full_graph(self, visited_edges):
        graph = self.instance.getGraph()
        edges_to_visit = self.instance.getEdges()
        current_vertex = self.instance.getStartPoint()

        if not all(item in visited_edges for item in edges_to_visit):
            return False

        for current_edge in visited_edges:
            edges = graph[current_vertex]
            if current_edge not in edges:
                return False

            current_vertex = edges[current_edge]

        return current_vertex == self.instance.getStartPoint()

    def constructSolution(self):
        current_vertex = self.instance.getStartPoint()
        visited_edges = []

        while not self.__has_traversed_full_graph(visited_edges):
            edges = list(self.instance.getPossbileNextEdgesByVertex(current_vertex).keys())
            # print('current vertex', current_vertex)
            # print('current edges', edges)

            chosen_edge = self.makeDecision(edges)

            current_vertex = self.instance.getNextVertex(current_vertex, chosen_edge)
            visited_edges.append(chosen_edge)

            # print('next vertex', current_vertex)
            # print('next edge', chosen_edge)
            # print('---------------------------')


start = timeit.default_timer()

instance = CPPInstance(20)
obj, components = Solve(antCls=CPPAnt, instance=instance, numIterations=1, numAnts=500, alpha=1, beta=1)

stop = timeit.default_timer()
print('Time: ', stop - start)

print(obj, components)
