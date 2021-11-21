import random
import numpy as np

from Library import ACS_Ant, Solve


class CPPInstance:
    def __init__(self, n,distance,goal_value,graph):
        self.n = n
        self.goal_value = goal_value
        self.distance = distance

        self.starting_point = 0
        self.graph = graph

    def getNumVertices(self):
        return self.n

    def getPossbileNextEdgesByVertex(self, vertex):
        return self.graph[vertex][self.graph[vertex] != 0]

    def getStartPoint(self):
        return 0

    def getGraph(self):
        return self.graph

    def getNextVertex(self, current_vertex, next_edge):
        return self.graph[current_vertex][next_edge]

    def get_goal_value(self):
        return self.goal_value

    def get_distance(self):
        return self.distance


class CPPAnt(ACS_Ant):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.value = 0
        self.last_node = 0
        #self.coin_amount = 0
        self.chosen_coins = [0]*len(self.instance.getGraph()[0]) #wie len(d)

        super().__init__(**kwargs)

    def getComponentCost(self, component): #123 muss 3zahlen returnen
        chosen_value = self.instance.get_distance()[self.current_vertex,component]
        if (self.instance.get_goal_value()- (self.value+chosen_value))*(sum(self.chosen_coins)) + 1 <= 0:
            return 100000
        return (self.instance.get_goal_value()- (self.value+chosen_value))*(sum(self.chosen_coins)) + 1
        #return self.instance.getWeight(*[component])

    def get_chosen_coins(self):
        return self.chosen_coins

    def constructSolution(self):
        current_vertex = self.instance.getStartPoint()
        self.current_vertex = current_vertex

        while self.value < self.instance.get_goal_value():
            if current_vertex in self.instance.getGraph()[list(self.instance.getGraph().keys())[-1]]:
                break

            vertices = list(self.instance.getPossbileNextEdgesByVertex(current_vertex))

            #das ruft im weiteren dann get component cost auf,
            chosen_vertex = self.makeDecision(vertices)
            self.chosen_coins[chosen_vertex % len(self.instance.getGraph()[0])-1] += 1

            self.value += self.instance.distance[current_vertex,chosen_vertex]

            current_vertex = chosen_vertex
            self.current_vertex = current_vertex


def create_distance(d,N):
    """
    Creates distance matrix

    :param d: coin denomiations
    :param N: amount to sum up to
    :return: distance matrix, distance = coin value
    """

    size = (N // d[0]) * len(d) + 2
    matrix = np.zeros((size, size))

    c = 1
    for row in range(1, size - len(d) - 1):
        matrix[row, 1 + len(d) * c:1 + len(d) * (c + 1)] = d
        if ((row) % len(d)) == 0:
            c += 1

    #matrix[:, -1] = 1
    matrix[0, 1:1 + len(d)] = d
    matrix[-1, -1] = 0
    return matrix

def create_graph(d,N):
    graph = {
        0: np.arange(1,len(d)+1)
    }
    size = (N // d[0])*len(d) + 2
    c = 1
    for i in range(1, size - len(d) - 1):
        graph[i] = np.arange(len(d)*c + 1, len(d)*(c+1) + 1)
        if i % len(d) == 0:
            c += 1
    return graph



d = [2, 3, 5,7,11,16]
N = 53
distance = create_distance(d,N)
graph = create_graph(d,N)
instance = CPPInstance(50,distance,goal_value=N,graph=graph)
obj, components = Solve(antCls=CPPAnt, instance=instance, numIterations=100, numAnts=10, alpha=1, beta=1)
coin_values = []
coins = np.zeros(len(d))
for component in components:
    value = distance[:,component][distance[:,component] !=0][0]
    coin_values.append(value)
    coins[d == value] += 1

print("Value: {} was created using {} coins ".format(sum(coin_values),len(coin_values)))
print("Chosen coins: {}".format(coins))

