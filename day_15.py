from itertools import permutations
from collections import defaultdict

with open("day_15.txt") as f:
    inputs = list(map(int, f.readline().strip().split(",")))


STEPS = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}

class EndOfCode(Exception):
    pass


class IntCode_Computer:
    def __init__(self):
        self.state = inputs[:]
        self.state += [0] * 10000
        self.pointer = 0
        self.rel_base = 0
        self.inputs = []

    def run(self, input_data=None):
        if input_data:
            self.put(input_data)
        while True:
            instr = str(self.state[self.pointer])
            opcode = int(instr[-2:])
            if opcode == 99:
                raise EndOfCode

            modes = []
            for i in range(3, STEPS[opcode] + 2):
                try:
                    modes.append(int(instr[-i]))
                except:
                    modes.append(0)

            params = []
            for i in range(1, STEPS[opcode]):
                if modes[i - 1] == 0:
                    params.append(self.state[self.pointer + i])
                elif modes[i - 1] == 1:
                    params.append(self.pointer + i)
                elif modes[i - 1] == 2:
                    params.append(self.state[self.pointer + i] + self.rel_base)
                else:
                    raise AssertionError("Unknown")


            if opcode == 1: # addition
                self.state[params[2]] = self.state[params[0]] + self.state[params[1]]
            elif opcode == 2: # multiplication
                self.state[params[2]] = self.state[params[0]] * self.state[params[1]]
            elif opcode == 3: # input
                self.state[params[0]] = self.inputs[0]
                del self.inputs[0]
            elif opcode == 4: # output
                self.pointer += 2
                return self.state[params[0]]
            elif opcode == 5: #jump_if_not
                if self.state[params[0]] != 0:
                    self.pointer = self.state[params[1]]
                    continue
            elif opcode == 6: #jump_if
                if self.state[params[0]] == 0:
                    self.pointer = self.state[params[1]]
                    continue
            elif opcode == 7: #smaller
                if self.state[params[0]] < self.state[params[1]]:
                    self.state[params[2]] = 1
                else:
                    self.state[params[2]] = 0
            elif opcode == 8: # equal
                if self.state[params[0]] == self.state[params[1]]:
                    self.state[params[2]] = 1
                else:
                    self.state[params[2]] = 0
            elif opcode == 9: # new_rel_base
                self.rel_base += self.state[params[0]]

            self.pointer += STEPS[opcode]

    def put(self, obj):
        self.inputs.append(obj)

def draw_grid(grid):
    x_bounds = (min(p[0] for p in grid), max(p[0] for p in grid) + 1, 1)
    y_bounds = (max(p[1] for p in grid), min(p[1] for p in grid) - 1, -1)
    
    for y in range(*y_bounds)[::-1]:
        output = ''
        for x in range(*x_bounds):
            output += "# OSo¤"[grid[(x,y)]]
        print(output)

def edit_surrounding_oxygen(grid, location):
    directions = [(-1,0),(0,1),(1,0),(0,-1)]
    for dirs in directions:
        if grid[(location[0]+dirs[0],location[1]+dirs[1])] == 1:
            grid[(location[0]+dirs[0],location[1]+dirs[1])] = 2
    grid[location] = 4
    return grid

def edit_surrounding_path(grid, location):
    directions = [(-1,0),(0,1),(1,0),(0,-1)]
    for dirs in directions:
        if grid[(location[0]+dirs[0],location[1]+dirs[1])] in [1,2]:
            grid[(location[0]+dirs[0],location[1]+dirs[1])] = 3
    grid[location] = 4
    return grid

def count_time_oxygen(grid):
    count = 0
    while 1 in grid.values():
        #draw_grid(grid)
        count += 1
        oxygen = [key for key in grid.keys() if grid[key] == 2]
        for location in oxygen:
            grid = edit_surrounding_oxygen(grid, location)

    return count

def count_time_start(grid):
    count = 0
    while 2 in grid.values():
        #draw_grid(grid)
        count += 1
        filled = [key for key in grid.keys() if grid[key] == 3]
        for location in filled:
            grid = edit_surrounding_path(grid, location)

    return count

def next_direciton(direction):
    if direction == 1:
        return 4
    elif direction == 2:
        return 3
    elif direction == 3:
        return 1
    elif direction == 4:
        return 2

def try_direction(direction):
    if direction == 1:
        return 3
    elif direction == 2:
        return 4
    elif direction == 3:
        return 2
    elif direction == 4:
        return 1

def map_the_area():
    moves = [(None, None), (0, -1), (0, 1), (-1, 0), (1, 0)]
    direction = 1
    location = [0,0]
    grid = defaultdict(lambda:0)
    grid[(0,0)] = 3
    pc = IntCode_Computer()
    first = True
    while location != [0,0] or first:
        
        output = pc.run(direction)
        if output == 0:
            grid[tuple([location[0]+moves[direction][0], location[1]+moves[direction][1]])] = 0
            direction = next_direciton(direction)
        elif output == 1:
            location = [location[0]+moves[direction][0], location[1]+moves[direction][1]]
            grid[tuple(location)] = 1
            first = False
            tmp_dir = try_direction(direction)
            output = pc.run(tmp_dir)
            if output == 1:
                direction = tmp_dir
                location = [location[0]+moves[direction][0], location[1]+moves[direction][1]]
                grid[tuple(location)] = 1
        elif output == 2:
            location = [location[0]+moves[direction][0], location[1]+moves[direction][1]]
            grid[tuple(location)] = 2

    grid[(0,0)] = 3
    #draw_grid(grid)
    return grid


if __name__ == "__main__":

    grid = map_the_area()
    draw_grid(grid)
    print('Part 1 = {}'.format(count_time_start(grid.copy())))
    print('Part 2 = {}'.format(count_time_oxygen(grid.copy())))