from math import sqrt
import Labyrinth as laby

def readFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    nbinstances = int(lines[0].strip())
    matrices = []
    nline = 1
    for _ in range(nbinstances):
        matrice = []
        n= int(lines[nline].strip().split(' ')[0])
        m= int(lines[nline].strip().split(' ')[1])
        nline += 1
        for i in range(n):
            matrice.append(list(lines[nline].strip()))
            nline += 1
        matrices.append(matrice)
    return nbinstances, matrices
            
class Graph:
    def __init__(self, matrice):
        self.verticesList = []
        self.adjacencyList = []
        for i in range(len(matrice)):
            for j in range(len(matrice[0])):
                if matrice[i][j] != '#':
                    self.addVertex((i, j))
                if matrice[i][j] == 'D':
                    self.start = (i, j)
                if matrice[i][j] == 'S':
                    self.end = (i, j)
                if matrice[i][j] == 'F':
                    self.flame = (i, j)
        # for each vertex, we add the edges connect to up, down, left, right vertices
        for i in range(len(self.verticesList)):
            x, y = self.verticesList[i]
            if x > 0 and matrice[x-1][y] != '#':
                self.addEdge(i, self.verticesList.index((x-1, y)))
            if x < len(matrice)-1 and matrice[x+1][y] != '#':
                self.addEdge(i, self.verticesList.index((x+1, y)))
            if y > 0 and matrice[x][y-1] != '#':
                self.addEdge(i, self.verticesList.index((x, y-1)))
            if y < len(matrice[0])-1 and matrice[x][y+1] != '#':
                self.addEdge(i, self.verticesList.index((x, y+1)))
        self.feuPath()
    def addEdge(self, u, v):
        self.adjacencyList[u].append(v)
        self.adjacencyList[v].append(u)
    def addVertex(self, x):
        self.verticesList.append(x)
        self.adjacencyList.append([])
    def minDistance(self, distance, visited):
        min = float('inf')
        min_index = -1
        for v in range(len(self.verticesList)):
            if distance[v] < min and not visited[v]:
                min = distance[v]
                min_index = v
        return min_index
    def dijkstra(self, start, end):
        start_index = self.verticesList.index(start)
        end_index = self.verticesList.index(end)
        distance = [float('inf')] * len(self.verticesList)
        distance[start_index] = 0
        visited = [False] * len(self.verticesList)
        previous = [None] * len(self.verticesList)
        number_of_vertices_explored = 0

        for _ in range(len(self.verticesList)):
            u = self.minDistance(distance, visited)
            if u == -1:
                break
            visited[u] = True
            for v in self.adjacencyList[u]:
                if not visited[v] and distance[v] > distance[u] + 1 and (distance[u]+1)<self.feuAllume[v]:
                    distance[v] = distance[u] + 1
                    previous[v] = u
            number_of_vertices_explored += 1


        path = []
        current = end_index
        while current is not None:
            path.insert(0, self.verticesList[current])
            current = previous[current]
        if distance[end_index] == float('inf'):
            print("No path found")
            return "N"
        else:
            print("Using Dijkstra")
            print("Number of vertices explored : ", len(path))
            return "Y"
    def heuristic(self, a, b):
        return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    def Astar(self, start, end):
        start_index = self.verticesList.index(start)
        end_index = self.verticesList.index(end)
        distance = [float('inf')] * len(self.verticesList)
        distance[start_index] = 0
        visited = [False] * len(self.verticesList)
        previous = [None] * len(self.verticesList)
        number_of_vertices_explored = 0
        

        for _ in range(len(self.verticesList)):
            u = self.minDistance(distance, visited)
            if u == -1:
                break
            visited[u] = True
            for v in self.adjacencyList[u]:
                if not visited[v] and distance[v] > distance[u] + 1 + self.heuristic(self.verticesList[u], self.verticesList[v]) and (distance[u] + 1) < self.feuAllume[v]:
                    distance[v] = distance[u] + 1
                    previous[v] = u
            number_of_vertices_explored += 1

        path = []
        current = end_index
        while current is not None:
            path.insert(0, self.verticesList[current])
            current = previous[current]
        if distance[end_index] == float('inf'):
            print("No path found")
            return "N"
        else:
            print("Using A*")
            print("Number of vertices explored : ", len(path))
            return "Y"

    def feuPath(self):
        self.feuAllume = [float('inf') for _ in range(len(self.verticesList))]
        self.feuAllume[self.verticesList.index(self.flame)] = 0
        queue = [self.flame]
        
        while queue:
            current = queue.pop(0)
            current_index = self.verticesList.index(current)
            for neighbor in self.adjacencyList[current_index]:
                if self.feuAllume[neighbor] == float('inf'):
                    self.feuAllume[neighbor] = self.feuAllume[current_index] + 1
                    queue.append(self.verticesList[neighbor])


if __name__ == '__main__':
    nbinstances, matrices = readFile('labyrinth.txt')
    for matrice in matrices:
        print(len(matrice))
        print(len(matrice[0]))
        print(matrice)
        graph = Graph(matrice)
        #path = graph.dijkstra(graph.start, graph.end)
        path = graph.Astar(graph.start, graph.end)
        #print(path)
        laby.draw_labyrinth(matrice)
        laby.draw_pathFlame(path)