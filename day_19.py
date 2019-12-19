from itertools import permutations
from collections import defaultdict

with open("day_19.txt") as f:
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
            output += chr(grid[(x,y)])
        print(output)

def test_for_coordinates(coordinates):
    pc = IntCode_Computer()
    pc.put(coordinates[0])
    pc.put(coordinates[1])
    output = pc.run()
    return output


def get_next_top(last_position):
    for cords in [(x, 1) for x in reversed(range(5))]:
        result = test_for_coordinates((last_position[0]+cords[0],last_position[1]+cords[1],))
        if result == 1:
            return (last_position[0]+cords[0],last_position[1]+cords[1],)
    return -1

def try_box(coordinates):

    the_point = test_for_coordinates((coordinates[0] - 99, coordinates[1]))
    
    if the_point == 1:
        bottom_point = test_for_coordinates((coordinates[0] - 99, coordinates[1]+99))
        if bottom_point == 1:
            return (coordinates[0] - 99 , coordinates[1])

    return -1    

def calculate_value(coordinates):
    return coordinates[0] * 10000 + coordinates[1]

def part_1():
    grid = {}
    count = 0
    for x in range(50):
        for y in range(50):
            result = test_for_coordinates((x,y))
            if result == 1:
                count += 1
                grid[(x,y)] = ord("#")
            else:
                grid[(x,y)] = ord(".")

    return count

def part_2():
    grid = {}
    y = 500
    leftmost = 0
    rightmost = 0
    started = False
    for x in range(500):
            result = test_for_coordinates((x,y))
            if result == 1:
                grid[(x,y)] = ord("#")
                if not started:
                    leftmost = x
                    started = True
            else:
                if started:
                    rightmost = x-1
                    started = False
                grid[(x,y)] = ord(".")

    lastpos = (rightmost, 500)
    while True:
        lastpos = get_next_top(lastpos)
        result = try_box(lastpos)
        if result != -1:
            return calculate_value(result)

if __name__ == "__main__":

    print('Part 1 = {}'.format(part_1()))
    print('Part 2 = {}'.format(part_2()))






