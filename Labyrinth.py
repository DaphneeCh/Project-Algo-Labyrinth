import tkinter as tk
import time
from Graph import Graph

class Labyrinth:
    def __init__(self, file_path):
        self.file_path = file_path
        self.instances = []
        self.root = tk.Tk()

    def read_file(self):
        with open(self.file_path) as f:
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
        self.instances = matrices

    def draw_labyrinth(self, grid, path=None, graph=None):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        cell_size = min(screen_width // (len(grid[0])+1), screen_height // (len(grid)+1))
        canvas_width = cell_size * len(grid[0])
        canvas_height = cell_size * len(grid)

        canva = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        canva.pack()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                color = 'white'
                if grid[i][j] == 'D':
                    color = 'green'
                elif grid[i][j] == 'S':
                    color = 'red'
                elif grid[i][j] == 'F':
                    color = 'orange'
                elif grid[i][j] == '#':
                    color = 'black'
                canva.create_rectangle(j*cell_size, i*cell_size, j*cell_size+cell_size, i*cell_size+cell_size, fill=color)
        def draw_path(x,y):
            canva.create_rectangle(y*cell_size, x*cell_size, y*cell_size+cell_size, x*cell_size+cell_size, fill='green')
        def draw_fire(x,y,color='orange'):
            canva.create_rectangle(y*cell_size, x*cell_size, y*cell_size+cell_size, x*cell_size+cell_size, fill=color)
        if path:
            for i in range(len(path)):
                canva.after(i*200, draw_path,*path[i])
                for j in range(len(graph.feuAllume)):
                    if graph.feuAllume[j] == i:
                        if graph.verticesList[j] in path:
                            canva.after(i*200, draw_fire,*graph.verticesList[j],'blue')
                        else:
                            canva.after(i*200, draw_fire,*graph.verticesList[j])

    def find_and_draw_path(self):
        for grid in self.instances:
            graph = Graph(grid)
            path = graph.dijkstra(graph.start, graph.end)
            #path = graph.Astar(graph.start, graph.end)
            graph.feuPath()
            self.draw_labyrinth(grid, path, graph)
        self.root.mainloop()
            

# Example usage:
labyrinth = Labyrinth('test.txt')
labyrinth.read_file()
labyrinth.find_and_draw_path()