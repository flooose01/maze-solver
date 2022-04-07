#THIS PROGRAM USES ELLER'S ALGORITHM TO GENERATE A MAZE
import random

WIDTH = 5
HEIGHT = 5
WALL = "w"
CELL = "c"

class Cell():
    def __init__(self, set, bottom = False, right = False):
        self.set = set
        self.bottom = bottom
        self.right = right

    def __repr__(self):
        return str(self.set)

def print_arr(arr):
    for r in arr:
        for c in r:
            print(c,end = " ")
        print()

def get_row(row_cells):
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

    return row + "\n"

def add_row(arr, row_cells):
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

    arr.append(row1)
    arr.append(row2)

final_maze = ""
final_arr = [[WALL for i in range(2 * WIDTH + 1)]]
curr_row = []
set_to_cells = {}

for i in range(WIDTH):
    cell = Cell(i)
    curr_row.append(cell)
    set_to_cells[i] = [cell]

for i in range(HEIGHT):

    for j in range(WIDTH - 1):
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

    curr_row[WIDTH - 1].right = True


    if i < HEIGHT - 1:
        for set in set_to_cells:
            bottom_count = 0
            for cell in set_to_cells[set]:
                create_bottom_wall = bool(random.getrandbits(1))
                if bottom_count < len(set_to_cells[set]) - 1 and create_bottom_wall:
                    cell.bottom = True
                    bottom_count += 1

        final_maze += get_row(curr_row)
        add_row(final_arr, curr_row)


        new_row = []
        new_set_to_cells = {}
        set_count = WIDTH * (i + 1)
        for cell in curr_row:
            if cell.bottom:
                new_cell = Cell(set_count)
                new_row.append(new_cell)
                if set_count in new_set_to_cells.keys():
                    new_set_to_cells[set_count].append(new_cell)
                else:
                    new_set_to_cells[set_count] = [new_cell]

                set_count += 1
            else:
                new_cell = Cell(cell.set)
                new_row.append(new_cell)
                
                if cell.set in new_set_to_cells.keys():
                    new_set_to_cells[cell.set].append(new_cell)
                else:
                    new_set_to_cells[cell.set] = [new_cell]
            
        curr_row = new_row
        set_to_cells = new_set_to_cells

    #FINISHING MAZE
    else:
        for j in range(WIDTH - 1):
            curr_cell = curr_row[j]
            next_cell = curr_row[j + 1]

            curr_cell.bottom = True

            if curr_cell.set != next_cell.set:
                curr_cell.right = False
                next_set_cells = set_to_cells.pop(next_cell.set)
                set_to_cells[curr_cell.set] += next_set_cells
                for cell in next_set_cells :
                    cell.set = curr_cell.set

        final_maze += get_row(curr_row)
        add_row(final_arr, curr_row)

print(final_maze)
print_arr(final_arr)

        




