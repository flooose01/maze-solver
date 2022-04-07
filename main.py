# TEST DFS BFS ON DIFFERENT MAZES
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from maze import Maze
from constants import WALL, CELL, VISITED, STATE_TO_COLOR
from maze import TYPES

class AnimationScreen(tk.Canvas):
    def __init__(self, master, maze_type, maze_width, maze_height, **kwargs):
        super().__init__(master, **kwargs)

        self.maze_manager = Maze(maze_type, maze_width, maze_height)
        self.animation_state = AnimationState(self.maze_manager)
        #self.maze = self.animation_state.init_maze

        self.canvas_width = kwargs["width"]
        self.canvas_height = kwargs["height"]
        self.maze_scale = int(min(self.canvas_height/maze_height, self.canvas_width/maze_width))
        self.gen_img()
        self.image_canvas = self.create_image(0,0,anchor=tk.NW, image=self.img)

        self.frame = 0

    def gen_img(self):
        maze_arr = self.animation_state.curr_maze
        arr = np.zeros((len(maze_arr) * self.maze_scale, len(maze_arr[0]) * self.maze_scale, 3), dtype=np.uint8)

        for row in range(len(maze_arr)):
            for col in range(len(maze_arr[0])):
                state = STATE_TO_COLOR[maze_arr[row][col]]
                pixel = np.full((self.maze_scale, self.maze_scale, 3), state)
                arr[row * self.maze_scale : (row + 1) * self.maze_scale, col * self.maze_scale : (col + 1) * self.maze_scale] = pixel

        self.img = ImageTk.PhotoImage(image = Image.fromarray(arr, 'RGB'))


    def update_img(self):
        self.gen_img()
        self.itemconfig(self.image_canvas, image=self.img)

    def reset(self):
        self.animation_state = AnimationState(self.maze_manager)

class AnimationState():
    def __init__(self, maze_manager):
        #maze_manager.maze = Eller()
        self.master_maze = maze_manager.maze
        self.init_maze = maze_manager.maze.get_maze()
        self.curr_maze = self.init_maze
        self.height = maze_manager.maze.height
        self.width = maze_manager.maze.width

        self.curr_pos = (1,1)
        self.visited = [(1,1)]
        self.st = [(1,1)]
        self.end_pos = (self.height - 1, self.width - 2)

    def get_curr_maze(self):
        return self.curr_maze

    def dfs(self):
        pos = self.st.pop(len(self.st) - 1)
        curr_y = pos[0]
        curr_x = pos[1]
        self.curr_maze[curr_y][curr_x] = VISITED

        # Find neighbors
        if self.curr_maze[curr_y][curr_x - 1] == self.CELL:
            self.st.append((curr_x - 1, curr_y))

        if self.curr_maze[curr_y + 1][curr_x] == self.CELL:
            self.st.append((curr_x, curr_y + 1))

        if self.curr_maze[curr_y][curr_x + 1] == self.CELL:
            self.st.append((curr_x + 1, curr_y))

        if self.curr_maze[curr_y - 1][curr_x] == self.CELL:
            self.st.append((curr_x, curr_y - 1))

        if (curr_y, curr_x) == self.end_pos:
            self.st.clear()


    def reset(self):
        self.curr_maze = self.init_maze
        self.curr_pos = (1,1)
        self.visited = [(1,1)]
        self.st = [(1, 1)]

class AnimationWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Header
        self.title("Maze Solver")
        self.geometry("800x640")
        self.resizable(False, False)

        # Menu screen
        self.right_frame = tk.Frame(self, width=160, height=640)
        self.right_frame.pack(side = tk.LEFT)
        self.right_frame.pack_propagate(0)

        # Type selection
        lbl1 = tk.Label(self.right_frame, text="Type", font=("Arial", 15),
            width=10, padx=2, pady=10)
        lbl1.pack()

        self.maze_type = tk.StringVar(self, "eller")
        type_buttons = {}
        for type in list(TYPES.keys()):
            button = tk.Radiobutton(self.right_frame, text=type, variable=self.maze_type,
                    value=type, font=("Arial", 12))
            button.pack()
            type_buttons[type] = button

        # Size selection
        tk.Label(self.right_frame, text="Width", bd=5, font=("Arial", 15),
            width=10, padx=2, pady=10).pack()
        maze_width = tk.IntVar(self, 5)
        self.maze_width_entry = tk.Entry(self.right_frame, textvariable=maze_width,
            font=("Arial", 12), bd=5)
        self.maze_width_entry.pack()

        tk.Label(self.right_frame, text="Height", bd=5, font=("Arial", 15),
            width=10, padx=2, pady=10).pack()
        maze_height = tk.IntVar(self, 5)
        self.maze_height_entry = tk.Entry(self.right_frame, textvariable=maze_height,
            font=("Arial", 12), bd=5)
        self.maze_height_entry.pack()

        def gen_animation_screen():
            # Animation screen
            try:
                mw = maze_width.get()
                mh = maze_height.get()
            except:
                mw = 5
                mh = 5

            self.animation_screen = AnimationScreen(self, maze_type=self.maze_type.get(),
                maze_width=mw, maze_height=mh, width = 640, height = 640)
            self.animation_screen.pack()

        # Generate button
        self.gen_button = tk.Button(self.right_frame, text="generate maze", pady=10,
            command=gen_animation_screen)
        self.gen_button.pack()

        #def start_animation():

        # Start button
        self.start_button = tk.Button(self.right_frame, text="start", pady=10, padx=20)
        self.start_button.pack()

        #def stop_animation():
        #test

        # Stop button
        self.stop_button = tk.Button(self.right_frame, text="stop", pady=10, padx=20)
        self.stop_button.pack()

def main():
    aw = AnimationWindow()
    aw.mainloop()

if __name__ == "__main__":
    main()
