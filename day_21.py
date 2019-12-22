from itertools import permutations
from collections import defaultdict

with open("day_21.txt") as f:
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


def part_1():
    pc = IntCode_Computer()
    
    # If A,B or C not Ground, and D Ground => Jump
    instructions = [
        "NOT A J\n",
        "NOT B T\n",
        "OR T J\n",
        "NOT C T\n",
        "OR T J\n",
        "AND D J\n",
        "WALK\n",
    ]

    for row in instructions:
        for letter in row:
            pc.put(ord(letter))

    halt = False
    while not halt:
        try:
            output = pc.run()
            try:
                #print(chr(output), end="")
                chr(output)
            except:
                return output
        except EndOfCode:
            halt = True

def part_2():
    pc = IntCode_Computer()

    # If A,B or C not Ground, and D Ground => Jump True
    # If E or H not Ground => Jump False
    instructions = [
        "NOT A J\n",
        "NOT B T\n",
        "OR T J\n",
        "NOT C T\n",
        "OR T J\n",
        "AND D J\n",
        "AND E T\n",
        "OR H T\n",
        "AND T J\n",
        "RUN\n",
    ]

    for row in instructions:
        for letter in row:
            pc.put(ord(letter))

    halt = False
    while not halt:
        try:
            output = pc.run()
            try:
                #print(chr(output), end="")
                chr(output)
            except:
                return output
        except EndOfCode:
            halt = True

if __name__ == "__main__":

    print('Part 1 = {}'.format(part_1()))
    print('Part 2 = {}'.format(part_2()))






