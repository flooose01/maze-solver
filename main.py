import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from copy import deepcopy
from maze import Maze, TYPES
from constants import PATH, CELL, VISITED, STATE_TO_COLOR

class AnimationScreen(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas_width = kwargs["width"]
        self.canvas_height = kwargs["height"]
        self.blank_img = ImageTk.PhotoImage(Image.new(mode="RGB",
            size=(self.canvas_width, self.canvas_height)))
        self.image_canvas = self.create_image(0,0,anchor=tk.NW,
            image=self.blank_img)
        self.is_animate = False
        self.maze_manager = Maze(type="eller", width=10, height=10)
        self.animation_state = AnimationState(self.maze_manager)
        self.maze_scale = int(min(self.canvas_height/10, self.canvas_width/10))

    def update_screen(self, maze_type, maze_width, maze_height):
        self.maze_manager = Maze(maze_type, maze_width, maze_height)
        self.animation_state = AnimationState(self.maze_manager)
        self.maze_scale = int(min(self.canvas_height/maze_height, self.canvas_width/maze_width))
        self.update_img()

    def update_img(self):
        maze_arr = self.animation_state.curr_maze
        arr = np.zeros((len(maze_arr) * self.maze_scale, len(maze_arr[0]) * self.maze_scale, 3),
            dtype=np.uint8)

        for row in range(len(maze_arr)):
            for col in range(len(maze_arr[0])):
                state = STATE_TO_COLOR[maze_arr[row][col]]
                pixel = np.full((self.maze_scale, self.maze_scale, 3), state)
                arr[row * self.maze_scale : (row + 1) * self.maze_scale,
                    col * self.maze_scale : (col + 1) * self.maze_scale] = pixel

        self.img = ImageTk.PhotoImage(image = Image.fromarray(arr, 'RGB'))
        self.itemconfig(self.image_canvas, image=self.img)

    def start_animate(self, animation_speed):
        self.is_animate = True
        self.animation_speed = animation_speed
        self.next_frame()

    def next_frame(self):
        if self.is_animate and not self.animation_state.is_finish:
            self.animation_state.dfs()
            self.update_img()
            self.after(self.animation_speed, self.next_frame)
            self.check_finish()

    def check_finish(self):
        if self.animation_state.is_finish:
            self.stop_animate()

    def stop_animate(self):
        self.is_animate = False

    def reset(self):
        self.animation_state.reset()
        self.update_img()

class AnimationState():
    def __init__(self, maze_manager):
        self.master_maze = maze_manager.maze
        self.init_maze = self.master_maze.get_maze()
        self.curr_maze = deepcopy(self.init_maze)
        self.height = self.master_maze.height
        self.width = self.master_maze.width

        self.is_finish = False
        self.curr_pos = (1,1)
        self.st = [(1,1)]
        self.path = []
        self.end_pos = (self.height - 1, self.width - 2)

    def dfs(self):
        pos = self.st[len(self.st) - 1]
        curr_y = pos[0]
        curr_x = pos[1]
        self.curr_maze[curr_y][curr_x] = VISITED

        if pos == self.end_pos:
            self.is_finish = True
            self.path.append(pos)
            for path in self.path:
                self.curr_maze[path[0]][path[1]] = PATH

        else:
            if self.is_dead_end(pos):
                self.st.pop()
                while (self.is_dead_end(self.st[len(self.st) - 1])):
                    self.st.pop()
                    self.path.pop()
            else:
                self.path.append(pos)
                # Find neighbors
                if self.curr_maze[curr_y][curr_x - 1] == CELL:
                    self.st.append((curr_y, curr_x - 1))

                if self.curr_maze[curr_y + 1][curr_x] == CELL:
                    self.st.append((curr_y + 1, curr_x))

                if self.curr_maze[curr_y][curr_x + 1] == CELL:
                    self.st.append((curr_y, curr_x + 1))

                if self.curr_maze[curr_y - 1][curr_x] == CELL:
                    self.st.append((curr_y - 1, curr_x))

    def is_dead_end(self, pos):
        curr_y = pos[0]
        curr_x = pos[1]

        if pos != self.end_pos:
            return (self.curr_maze[curr_y][curr_x - 1] != CELL and self.curr_maze[curr_y + 1][curr_x] != CELL
                and self.curr_maze[curr_y][curr_x + 1] != CELL and self.curr_maze[curr_y - 1][curr_x] != CELL)
        else:
            return False

    def reset(self):
        self.is_finish = False
        self.curr_maze = deepcopy(self.init_maze)
        self.curr_pos = (1,1)
        self.visited = [(1,1)]
        self.st = [(1, 1)]

class AnimationWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Constants
        self.DEFAULT_SIZE = (10, 10)
        self.ANIMATION_SPEED = [2000, 1000, 100, 10, 1]

        # Header
        self.title("Maze Solver")
        self.geometry("900x640")

        # Menu screen
        self.menu_frame = tk.Frame(self, width=260, height=640)
        self.menu_frame.pack(side = tk.LEFT)
        self.menu_frame.pack_propagate(0)

        # Type selection
        tk.Label(self.menu_frame, text="Type", font=("Arial", 15),
            width=10, pady=10, bd=2, relief="solid").pack()

        self.type_frame = tk.Frame(self.menu_frame, width=260, height=150)
        self.type_frame.pack()

        self.maze_type = tk.StringVar(self, list(TYPES.keys())[0])
        self.type_buttons = {}
        i = -1
        for type in list(TYPES.keys()):
            i += 1
            button = tk.Radiobutton(self.type_frame, text=type, variable=self.maze_type,
                    value=type, font=("Arial", 12))
            button.grid(column=i%3, row=int(i/3))
            self.type_buttons[type] = button

        # Size selection
        tk.Label(self.menu_frame, text="Size", font=("Arial", 15),
            width=10, pady=10, bd=2, relief="solid").pack()

        self.size_frame = tk.Frame(self.menu_frame, width=260, height=150)
        self.size_frame.pack()

        tk.Label(self.size_frame, text="Width", font=("Arial", 12),
            width=10).grid(column=0, row=0)
        self.maze_width = tk.IntVar(self, self.DEFAULT_SIZE[0])
        self.maze_width_entry = tk.Entry(self.size_frame, textvariable=self.maze_width,
            font=("Arial", 10), bd=5, width=4)
        self.maze_width_entry.grid(column=0, row=1)

        tk.Label(self.size_frame, text="Height", font=("Arial", 12),
            width=10).grid(column=1, row=0)
        self.maze_height = tk.IntVar(self, self.DEFAULT_SIZE[1])
        self.maze_height_entry = tk.Entry(self.size_frame, textvariable=self.maze_height,
            font=("Arial", 10), bd=5, width=4)
        self.maze_height_entry.grid(column=1, row=1)

        # Speed
        tk.Label(self.menu_frame, text = "Speed", font=("Arial", 15),
            width=10, pady=10, bd=2, relief="solid").pack()
        self.speed_slider = tk.Scale(self.menu_frame, from_=1, to=len(self.ANIMATION_SPEED),
            orient='horizontal')
        self.speed_slider.set(3)
        self.speed_slider.pack()

        # Initialize animation screen
        self.animation_screen = AnimationScreen(self, width=640, height=640)
        self.animation_screen.pack()

        # Control
        tk.Label(self.menu_frame, text="Control", font=("Arial", 15),
            width=10, pady=10, bd=2, relief="solid").pack()

        self.control_frame = tk.Frame(self.menu_frame, width=260, height=340)
        self.control_frame.pack()

        def generate_maze():
            try:
                mw = self.maze_width.get()
                mh = self.maze_height.get()
            except:
                mw = self.DEFAULT_SIZE[0]
                mh = self.DEFAULT_SIZE[1]

            self.animation_screen.update_screen(maze_type=self.maze_type.get(),
                maze_width=mw, maze_height=mh)

            self.start_button.configure(state="normal")
            self.reset_button.configure(state="disabled")

        # Generate button
        self.gen_button = tk.Button(self.control_frame, text="generate maze", pady=10,
            command=generate_maze)
        self.gen_button.grid(column=1, row=0, pady=5)

        def start_animate():
            self.animation_screen.start_animate(
                animation_speed=self.ANIMATION_SPEED[self.speed_slider.get()-1])
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.gen_button.configure(state="disabled")
            self.reset_button.configure(state="disabled")
            self.speed_slider.configure(state="disabled")
            self.maze_height_entry.configure(state="disabled")
            self.maze_width_entry.configure(state="disabled")
            for but in self.type_buttons.values():
                but.configure(state="disabled")

        # Start button
        self.start_button = tk.Button(self.control_frame, text="start", pady=10, padx=20,
            command=start_animate, state="disabled")
        self.start_button.grid(column=0, row=1)

        def stop_animate():
            self.animation_screen.stop_animate()
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.gen_button.configure(state="normal")
            self.reset_button.configure(state="normal")
            self.speed_slider.configure(state="normal")
            self.maze_height_entry.configure(state="normal")
            self.maze_width_entry.configure(state="normal")
            for but in self.type_buttons.values():
                but.configure(state="normal")

        # Stop button
        self.stop_button = tk.Button(self.control_frame, text="stop", pady=10, padx=20,
            command=stop_animate, state="disabled")
        self.stop_button.grid(column=1, row=1)

        def reset():
            self.animation_screen.reset()
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

        self.reset_button = tk.Button(self.control_frame, text="reset", pady=10, padx=20,
            command=reset, state="disabled")
        self.reset_button.grid(column=2, row=1)

def main():
    aw = AnimationWindow()
    aw.mainloop()

if __name__ == "__main__":
    main()
