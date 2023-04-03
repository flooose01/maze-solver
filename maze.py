#Generate mazes with different algorithm

import random
from constants import WALL, CELL

class Maze:
    def __init__(self, type, width, height):
        self.maze_width = width
        self.maze_height = height
        self.type = type
        self.maze = TYPES[type](width, height)

    def __repr__(self):
        return self.maze.__repr__()

class Eller:
    class Cell():
        def __init__(self, set, bottom = False, right = False):
            self.set = set
            self.bottom = bottom
            self.right = right

        def __repr__(self):
            return str(self.set)

    def __init__(self, width, height):
        self.virtual_width = int((width - 1) / 2)
        self.virtual_height = int((height - 1) / 2)
        self.width = self.virtual_width * 2 + 1
        self.height = self.virtual_height * 2 + 1
        self.final_arr = []
        self.final_maze = ""
        self.generate_maze()

    def __repr__(self):
        return self.show_maze_arr()

    def show_maze_arr(self):
        res = ""
        for r in self.final_arr:
            for c in r:
                res += c + " "
            res += "\n"

        return res

    def show_maze_str(self):
        return self.final_maze

    def get_maze(self):
        return self.final_arr

    def add_row_str(self, row_cells):
        row = "|"
        for cell in row_cells:
            if cell.bottom:
                row += " \u0332"
            else:
                row += " "

            row += str(cell)

            if cell.right:
                row += " |"
            else:
                row += "  "

        self.final_maze += row + "\n"

    def add_row_arr(self, row_cells):
        row1 = [WALL]
        row2 = [WALL]
        for cell in row_cells:
            if cell.bottom and cell.right:
                row1 += [CELL, WALL]
                row2 += [WALL, WALL]
            elif cell.bottom and not cell.right:
                row1 += [CELL, CELL]
                row2 += [WALL, WALL]
            elif not cell.bottom and cell.right:
                row1 += [CELL, WALL]
                row2 += [CELL, WALL]
            else:
                row1 += [CELL, CELL]
                row2 += [CELL, WALL]

        self.final_arr.append(row1)
        self.final_arr.append(row2)

    def generate_maze(self):
        self.final_arr = [[WALL for i in range(2 * self.virtual_width + 1)]]

        self.final_maze = ""
        curr_row = []
        set_to_cells = {}

        for i in range(self.virtual_width):
            cell = self.Cell(i)
            curr_row.append(cell)
            set_to_cells[i] = [cell]

        for i in range(self.virtual_height):

            for j in range(self.virtual_width - 1):
                curr_cell = curr_row[j]
                next_cell = curr_row[j + 1]

                create_right_wall = bool(random.getrandbits(1))
                if curr_cell.set == next_cell.set or create_right_wall:
                    curr_cell.right = True
                else:
                    next_set_cells = set_to_cells.pop(next_cell.set)
                    set_to_cells[curr_cell.set] += next_set_cells
                    for cell in next_set_cells :
                        cell.set = curr_cell.set

            curr_row[self.virtual_width - 1].right = True


            if i < self.virtual_height - 1:
                for set in set_to_cells:
                    bottom_count = 0
                    for cell in set_to_cells[set]:
                        create_bottom_wall = bool(random.getrandbits(1))
                        if bottom_count < len(set_to_cells[set]) - 1 and create_bottom_wall:
                            cell.bottom = True
                            bottom_count += 1

                self.add_row_str(curr_row)
                self.add_row_arr(curr_row)

                new_row = []
                new_set_to_cells = {}
                set_count = self.virtual_width * (i + 1)
                for cell in curr_row:
                    if cell.bottom:
                        new_cell = self.Cell(set_count)
                        new_row.append(new_cell)
                        if set_count in new_set_to_cells.keys():
                            new_set_to_cells[set_count].append(new_cell)
                        else:
                            new_set_to_cells[set_count] = [new_cell]

                        set_count += 1
                    else:
                        new_cell = self.Cell(cell.set)
                        new_row.append(new_cell)

                        if cell.set in new_set_to_cells.keys():
                            new_set_to_cells[cell.set].append(new_cell)
                        else:
                            new_set_to_cells[cell.set] = [new_cell]

                curr_row = new_row
                set_to_cells = new_set_to_cells

            #FINISHING MAZE
            else:
                for j in range(self.virtual_width - 1):
                    curr_cell = curr_row[j]
                    next_cell = curr_row[j + 1]

                    curr_cell.bottom = True
                    #next_cell.bottom = True

                    if curr_cell.set != next_cell.set:
                        curr_cell.right = False
                        next_set_cells = set_to_cells.pop(next_cell.set)
                        set_to_cells[curr_cell.set] += next_set_cells
                        for cell in next_set_cells :
                            cell.set = curr_cell.set

                self.add_row_str(curr_row)
                self.add_row_arr(curr_row)

class DFS:
    def __init__(self):
        self.test = 0

class Prim:
    def __init__(self):
        self.test = 0
        self.foo = "bar"

class Kruskal:
    def __init__(self):
        self.test = 0

TYPES = {"eller" : Eller, "dfs": DFS, "prim" : Prim, "kruskal" : Kruskal}