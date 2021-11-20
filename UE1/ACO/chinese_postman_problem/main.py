import random

from ACO.chinese_postman_problem.library import ACS_Ant, Solve


class CPPInstance:
    def __init__(self, n):
        self.n = n

        self.starting_point = 'a'

        self.graph = {
            'a': {1: 'b', 2: 'b'},
            'b': {3: 'c', 4: 'c'},
            'c': {7: 'a', 5: 'd'},
            'd': {6: 'c'}
        }

        self.edge_weights = {
            1: 4,
            2: 8,
            3: 5,
            4: 9,
            5: 3,
            6: 2,
            7: 6
        }

        self.xcoord = [random.random() * 100 for v in range(n)]
        self.ycoord = [random.random() * 100 for v in range(n)]

    def getNumVertices(self):
        return self.n

    def getWeight(self, edge):
        return self.edge_weights[edge]

    def getEdges(self):
        return self.edge_weights.keys()

    def getPossbileNextEdgesByVertex(self, vertex):
        return self.graph[vertex]

    def getStartPoint(self):
        return 'a'

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
            print('ant', id(self) % 100)
            print('current vertex', current_vertex)
            print('current edges', edges)

            chosen_edge = self.makeDecision(edges)

            current_vertex = self.instance.getNextVertex(current_vertex, chosen_edge)
            visited_edges.append(chosen_edge)

            print('next vertex', current_vertex)
            print('next edge', chosen_edge)
            print('---------------------------')


instance = CPPInstance(50)
obj, components = Solve(antCls=CPPAnt, instance=instance, numIterations=1000, numAnts=10, alpha=1, beta=1)
print(obj, components)
