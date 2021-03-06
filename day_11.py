from itertools import permutations
from collections import defaultdict

with open("day_11.txt") as f:
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

    def run(self):
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


if __name__ == "__main__":

    grid = defaultdict(lambda:0)
    pc = IntCode_Computer()
    seen = set()
    x, y, direction = 0, 0, 0
    ds = [(0,1),(1,0),(0,-1),(-1,0)]

    halt = False
    while not halt:
        try:
            pc.put(grid[(x,y)])

            color = pc.run()
            grid[(x,y)] = color
            seen.add((x,y))
            turn = pc.run()
            if turn == 0:
                direction = (direction - 1) % 4
            else:
                direction = (direction + 1) % 4
            x += ds[direction][0]
            y += ds[direction][1]
        except EndOfCode:
            halt = True


    print('Part 1 = {}'.format(len(seen)))

    grid = defaultdict(lambda:0)
    grid[(0,0)] = 1
    pc = IntCode_Computer()
    x, y, direction = 0, 0, 0
    ds = [(0,1),(1,0),(0,-1),(-1,0)]

    halt = False
    while not halt:
        try:
            pc.put(grid[(x,y)])

            color = pc.run()
            grid[(x,y)] = color
            turn = pc.run()
            if turn == 0:
                direction = (direction - 1) % 4
            else:
                direction = (direction + 1) % 4
            x += ds[direction][0]
            y += ds[direction][1]
        except EndOfCode:
            halt = True

    x_bounds = (min(p[0] for p in grid) - 1, max(p[0] for p in grid) + 2, 1)
    y_bounds = (max(p[1] for p in grid) + 1, min(p[1] for p in grid) - 2, -1)
    
    print('Part 2 = ')
    for y in range(*y_bounds):
        output = ''
        for x in range(*x_bounds):
            output += " #"[grid[(x,y)]]
        print(output)






