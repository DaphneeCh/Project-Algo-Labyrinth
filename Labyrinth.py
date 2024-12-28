import tkinter as tk
import time
from Graph import Graph

class Labyrinth:
    def __init__(self, file_path):
        self.file_path = file_path
        self.instances = []
        self.root = tk.Tk()
        self.window_width = self.root.winfo_screenwidth()*0.8
        self.window_height = self.root.winfo_screenheight()*0.8
        self.current_window = None
        self.current_canvas = None
        self.delay = 200

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

    def draw_labyrinth(self, grid, name, cell_size):
        if self.current_window:
            self.current_window.destroy()

        self.current_window = tk.Toplevel(self.root)
        canvas_width = cell_size * len(grid[0])
        canvas_height = cell_size * len(grid)+65
        self.current_canvas = tk.Canvas(self.current_window, width=canvas_width, height=canvas_height)
        self.current_canvas.pack()

        # Title
        self.current_canvas.create_text(canvas_width//2, canvas_height - 40, text=name, font=('Arial', 20))

        # Draw the grid
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
                self.current_canvas.create_rectangle(j*cell_size, i*cell_size, j*cell_size+cell_size, i*cell_size+cell_size, fill=color,tags='background')

    def draw_path(self, cell_size, path, graph: Graph, number_of_vertices_explored):
        canva = self.current_canvas
        # Draw path, draw fire function
        def draw_fire(x,y):
            rect_id = canva.create_rectangle(y*cell_size, x*cell_size, y*cell_size+cell_size, x*cell_size+cell_size, fill='orange',tags='fire')
            canva.tag_raise(rect_id,'background')
        def draw_step(x,y):
            oval_id = canva.create_oval(y*cell_size+cell_size//5, x*cell_size+cell_size//5, y*cell_size+cell_size*4//5, x*cell_size+cell_size*4//5, fill='green',tags='path')
            canva.tag_raise(oval_id,'background')
            canva.tag_raise(oval_id,'fire')
        def draw_die(x,y):
            xmark1 = canva.create_line(y*cell_size+cell_size//5, x*cell_size+cell_size//5, y*cell_size+cell_size*4//5, x*cell_size+cell_size*4//5, fill='red', width=cell_size//10, tags='path')
            xmark2 = canva.create_line(y*cell_size+cell_size*4//5, x*cell_size+cell_size//5, y*cell_size+cell_size//5, x*cell_size+cell_size*4//5, fill='red', width=cell_size//10, tags='path')
            canva.tag_raise(xmark1,'fire')
            canva.tag_raise(xmark2,'fire')
        def draw_lose_noti():
            noti_id = canva.create_text(canva.winfo_reqwidth()//2, canva.winfo_reqheight()//2, text='Path failed !', font=('Arial', 40), fill='red',tags='noti')
            canva.tag_raise(noti_id,'path')
        def draw_win_noti():
            noti_id = canva.create_text(canva.winfo_reqwidth()//2, canva.winfo_reqheight()//2, text='Path finished !', font=('Arial', 40), fill='green',tags='noti')
            canva.tag_raise(noti_id,'path')
        
        self.current_canvas.create_text(canva.winfo_reqwidth()//2, canva.winfo_reqheight() - 15, text="Number of vertices explored:"+str(number_of_vertices_explored), font=('Arial', 20))

        # Draw the path with the fire
        if len(path) > 0:
            win = True
            for i in range(len(path)):
                # Draw the fire
                for j in range(len(graph.feuAllume)):
                    if graph.feuAllume[j] == i:
                        canva.after(i*self.delay, draw_fire,*graph.verticesList[j])
                # Draw the path
                idx = graph.verticesList.index(path[i])
                if graph.feuAllume[idx] <= i:
                    if path[i] == graph.end:
                        canva.after(i*self.delay, draw_step,*path[i])
                    else:
                        canva.after(i*self.delay, draw_die,*path[i])
                        win = False
                        break
                else: 
                    canva.after(i*self.delay, draw_step,*path[i])
            # Draw the notification
            if win:
                canva.after(i*self.delay, draw_win_noti)
            else:
                canva.after(i*self.delay, draw_lose_noti)
        else:
            canva.create_text(canva.winfo_reqwidth()//2, canva.winfo_reqheight()//2, text='No path found', font=('Arial', 40), fill='red')

    def find_and_draw_path(self, idx, algorithm,name=None):
        grid = self.instances[idx-1]
        graph = Graph(grid)
        number_of_vertices_explored = 0
        if algorithm == 'dijkstra':
            path,number_of_vertices_explored = graph.dijkstra(graph.start, graph.end)
        elif algorithm == 'astar_distance':
            path,number_of_vertices_explored = graph.AstarDistance(graph.start, graph.end)
        elif algorithm == 'astar_fire':
            path,number_of_vertices_explored = graph.AstarFire(graph.start, graph.end)

        # Draw the labyrinth
        cell_size = min(self.window_width // (len(grid[0])+1), self.window_height // (len(grid)+1))
        self.draw_labyrinth(grid, name, cell_size)
        # Draw the path
        self.draw_path(cell_size, path, graph, number_of_vertices_explored)
    
    def draw_menu(self):
        # Create a menu with buttons for each maze instance
        self.root.title('Labyrinth')
        n = len(self.instances)
        self.root.geometry('600x'+str(int(n*45)))

        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(1, len(self.instances) + 1):
            name1 = 'Labyrinth ' + str(i) + '\nDijkstra' 
            button1 = tk.Button(frame, text=name1, command=lambda idx=i,name=name1:self.find_and_draw_path(idx, 'dijkstra',name))
            button1.grid(row=i, column=0)
            name2 = 'Labyrinth ' + str(i) + '\nA-star with distance heuristic'
            button2 = tk.Button(frame, text=name2, command=lambda idx=i,name=name2:self.find_and_draw_path(idx, 'astar_distance',name))
            button2.grid(row=i, column=1)
            name3 = 'Labyrinth ' + str(i) + '\nA-star with fire detection heuristic'
            button3 = tk.Button(frame, text=name3, command=lambda idx=i,name=name3:self.find_and_draw_path(idx, 'astar_fire',name))
            button3.grid(row=i, column=2)
    
        self.root.mainloop()

# Example usage:
labyrinth = Labyrinth('labyrinth.txt')
labyrinth.read_file()
labyrinth.draw_menu()