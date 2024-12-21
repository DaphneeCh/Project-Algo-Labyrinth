import tkinter as tk
from Graph import *

class Labyrinth:
    def __init__(self, file_path):
        self.file_path = file_path
        self.instances = []

    def read_file(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            T = int(lines[0].strip())
            index = 1
            for _ in range(T):
                N, M = map(int, lines[index].strip().split())
                index += 1
                grid = []
                for _ in range(N):
                    grid.append(list(lines[index].strip()))
                    index += 1
                self.instances.append((N, M, grid))

    def draw_labyrinth(self, graph):
        root = tk.Tk()
        self.canvas = tk.Canvas(root, width=20*len(matrice[0]), height=20*len(matrice))
        self.canvas.pack()
        for i in range(len(graph.verticesList)):
            self.canvas.create_rectangle(i*20, 0, i*20+20, 20, fill='white')
        self.canvas.create_rectangle(graph.start, 20, 20, fill='red')   
        self.canvas.create_rectangle(graph.end, 20, 20, fill='green')
        self.canvas.create_rectangle(graph.flame, 20, 20, fill='yellow')

        
    def draw_pathFlame(self, pathFlame):
        for i in range(len(pathFlame)-1):
            x1, y1 = self.verticesList[pathFlame[i]]
            x2, y2 = self.verticesList[pathFlame[i+1]]
            self.canvas.create_line(y1*20+10, x1*20+10, y2*20+10, x2*20+10, fill='red')

    
        
       
    


# Example usage:
laby = Labyrinth('test.txt')
laby.read_file()
for instance in laby.instances:
    N, M, grid = instance
    laby.draw_labyrinth(grid)
    