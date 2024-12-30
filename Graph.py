from math import sqrt
# Classe Graph
class Graph:
    '''
    Classe Graph
    Cette classe est utilisée pour représenter un graphe non orienté.
    Attributes:
    verticesList: list
        Une liste de tuples représentant les sommets du graphe.
    adjacencyList: list
        Une liste d'adjacence représentant les arêtes du graphe.
    start: tuple
        La position de départ.
    end: tuple
        La position d'arrivée.
    flame: tuple
        La position du feu.
    onFire: list
        Une liste représentant la distance de chaque sommet par rapport au feu.
    Methods:
    addEdge(u, v)
        Ajoute une arête entre les sommets u et v.
    addVertex(x)
        Ajoute un sommet x au graphe.
    minScore(score, visited)
        Retourne l'indice du sommet non visité ayant le score minimum.
    dijkstra(start, end)
        Retourne le chemin le plus court entre les sommets start et end en utilisant l'algorithme de Dijkstra.
    euclidean_distance_heuristic(a, b)
        Retourne la distance euclidienne entre les sommets a et b.
    Taxicab_distance_heuristic(a, b)
        Retourne la distance de Manhattan entre les sommets a et b.
    AstarDistance(start, end)
        Retourne le chemin le plus court entre les sommets start et end en utilisant l'algorithme A* avec la distance euclidienne comme heuristique.
    AstarFire(start, end)
        Retourne le chemin le plus court entre les sommets start et end en utilisant l'algorithme A* avec la détection du feu comme heuristique.
    traverseFirePath()
        Parcourt le graphe pour détecter la distance de chaque sommet par rapport au feu.
    '''
    def __init__(self, matrice):
        '''
        Constructeur de la classe Graph
        :param matrice: La matrice représentant le labyrinthe
        '''
        self.flame = None
        self.onFire = []
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
        # pour chaque sommet, nous ajoutons les arêtes connectant les sommets en haut, en bas, à gauche, à droite
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
        self.traverseFirePath()

    def addEdge(self, u, v):
        '''
        Ajoute une arête entre les sommets u et v.
        :param u: int'''
        self.adjacencyList[u].append(v)
        self.adjacencyList[v].append(u)

    def addVertex(self, x):
        '''
        Ajoute un sommet x au graphe.
        :param x: tuple'''
        self.verticesList.append(x)
        self.adjacencyList.append([])

    def minScore(self, score, visited):
        ''' 
        Retourne l'indice du sommet non visité ayant le score minimum.
        :param score: list
        :param visited: list
        :return: min_index: int 
        '''
        min = float('inf')
        min_index = -1
        for v in range(len(self.verticesList)):
            if score[v] < min and not visited[v]:
                min = score[v]
                min_index = v
        return min_index
    
    def dijkstra(self, start, end):
        '''
        Retourne le chemin le plus court entre les sommets start et end en utilisant l'algorithme de Dijkstra.
        :param start: tuple
        :param end: tuple
        :return: path: list
        :return: number_of_vertices_explored: int
        '''
        start_index = self.verticesList.index(start)
        end_index = self.verticesList.index(end)
        distance = [float('inf')] * len(self.verticesList)
        distance[start_index] = 0
        visited = [False] * len(self.verticesList)
        previous = [None] * len(self.verticesList)
        number_of_vertices_explored = 0

        for _ in range(len(self.verticesList)):
            u = self.minScore(distance, visited)
            if u == -1 or u == end_index:
                break
            visited[u] = True
            for v in self.adjacencyList[u]:
                if not visited[v] and distance[v] > distance[u] + 1:
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
        else:
            print("Using Dijkstra")
            print("Number of vertices explored : ", number_of_vertices_explored)
            print("Path length : ", len(path))
        return path,number_of_vertices_explored

    def euclidean_distance_heuristic(self, a, b): 
        '''
        Retourne la distance euclidienne entre les sommets a et b.
        :param a: tuple
        :param b: tuple
        :return: float
        '''
        return (a[0] - b[0])**2 + (a[1] - b[1])**2
    
    def Taxicab_distance_heuristic(self, a, b): 
        '''
        Retourne la distance de Manhattan entre les sommets a et b.
        :param a: tuple
        :param b: tuple
        :return: int
        '''
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def AstarDistance(self, start, end):
        '''
        Retourne le chemin le plus court entre les sommets start et end en utilisant l'algorithme A* avec la distance euclidienne comme heuristique.
        :param start: tuple
        :param end: tuple
        :return: path: list
        :return: number_of_vertices_explored: int'''
        start_index = self.verticesList.index(start)
        end_index = self.verticesList.index(end)
        distance = [float('inf')] * len(self.verticesList) # gScore
        distance[start_index] = 0
        fscore = [float('inf')] * len(self.verticesList) # fScore
        fscore[start_index] = self.euclidean_distance_heuristic(start, end)
        visited = [False] * len(self.verticesList)
        previous = [None] * len(self.verticesList)
        number_of_vertices_explored = 0
        
        for _ in range(len(self.verticesList)):
            u = self.minScore(fscore, visited)
            if u == -1 or u == end_index:
                break
            visited[u] = True
            for v in self.adjacencyList[u]:
                if not visited[v] and distance[v] > distance[u] + 1:
                    distance[v] = distance[u] + 1 # mettre à jour gScore
                    fscore[v] = distance[v] + self.euclidean_distance_heuristic(self.verticesList[v], end) # mettre à jour fScore
                    previous[v] = u # mettre à jour previous
            number_of_vertices_explored += 1

        path = []
        current = end_index
        while current is not None:
            path.insert(0, self.verticesList[current])
            current = previous[current]
        if distance[end_index] == float('inf'):
            print("No path found")
        else:
            print("Using A* with distance heuristic")
            print("Number of vertices explored : ", number_of_vertices_explored)
            print("Path length : ", len(path))
        return path,number_of_vertices_explored

    def AstarFire(self, start, end):
        '''
        Retourne le chemin le plus court entre les sommets start et end en utilisant l'algorithme A* avec la détection du feu comme heuristique.
        :param start: tuple
        :param end: tuple
        :return: path: list
        :return: number_of_vertices_explored: int'''
        start_index = self.verticesList.index(start)
        end_index = self.verticesList.index(end)
        distance = [float('inf')] * len(self.verticesList) # gScore
        distance[start_index] = 0
        fscore = [float('inf')] * len(self.verticesList) # fScore
        fscore[start_index] = self.euclidean_distance_heuristic(start, end)
        visited = [False] * len(self.verticesList)
        previous = [None] * len(self.verticesList)
        number_of_vertices_explored = 0

        for _ in range(len(self.verticesList)):
            u = self.minScore(fscore, visited)
            if u == -1 or u == end_index:
                break
            visited[u] = True
            for v in self.adjacencyList[u]:
                if not visited[v] and distance[v] > distance[u] + 1 and self.onFire[v] >= distance[u] + 1:
                    if self.onFire[v] == distance[u] + 1 and self.verticesList[v] != end:
                        continue
                    distance[v] = distance[u] + 1 # update gScore
                    fscore[v] = distance[v] + self.euclidean_distance_heuristic(self.verticesList[v], end) # update fScore
                    previous[v] = u # update previous
            number_of_vertices_explored += 1

        path = []
        current = end_index
        while current is not None:
            path.insert(0, self.verticesList[current])
            current = previous[current]
        if distance[end_index] == float('inf'):
            print("No path found")
        else:
            print("Using A* with fire detection heuristic")
            print("Number of vertices explored : ", number_of_vertices_explored)
            print("Path length : ", len(path))
        return path,number_of_vertices_explored

    def traverseFirePath(self):
        self.onFire = [float('inf') for _ in range(len(self.verticesList))]
        if self.flame == None:
            return
        self.onFire[self.verticesList.index(self.flame)] = 0
        queue = [self.flame]
        
        while queue:
            current = queue.pop(0)
            current_index = self.verticesList.index(current)
            for neighbor in self.adjacencyList[current_index]:
                if self.onFire[neighbor] == float('inf'):
                    self.onFire[neighbor] = self.onFire[current_index] + 1
                    queue.append(self.verticesList[neighbor])
