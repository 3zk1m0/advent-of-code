from itertools import permutations
from collections import defaultdict

with open("day_13.txt") as f:
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



"""
0 is an empty tile. No game object appears in this tile.            " "
1 is a wall tile. Walls are indestructible barriers.                "W"
2 is a block tile. Blocks can be broken by the ball.                "#
3 is a horizontal paddle tile. The paddle is indestructible.        "X"
4 is a ball tile. The ball moves diagonally and bounces off objects."O"
"""

if __name__ == "__main__":

    print('Part 1 = ')
    pc = IntCode_Computer()
    grid = defaultdict(lambda:0)


    halt = False
    while not halt:
        try:

            block_x = pc.run()
            block_y = pc.run()
            block_id = pc.run()


            grid[(block_x,block_y)] = block_id

        except EndOfCode:
            halt = True

    x_bounds = (min(p[0] for p in grid) - 1, max(p[0] for p in grid) + 2, 1)
    y_bounds = (max(p[1] for p in grid) + 1, min(p[1] for p in grid) - 2, -1)
    
    count = 0

    
    for y in range(*y_bounds)[::-1]:
        output = ''
        for x in range(*x_bounds):
            output += ' W#XO'[grid[(x,y)]]
            if ' W#XO'[grid[(x,y)]] == '#':
                count += 1
        print(output)
    print('Count = {}'.format(count))


    """
    If the joystick is in the neutral position, provide 0.
    If the joystick is tilted to the left, provide -1.
    If the joystick is tilted to the right, provide 1.
    """
    # Part 2
    pc = IntCode_Computer()
    pc.state[0] = 2
    grid = defaultdict(lambda:0)

    ball = 0
    paddle = 0
    frame_done = [False, False]

    halt = False
    while not halt:
        try:
            block_x = pc.run()
            block_y = pc.run()
            block_id = pc.run()

            if block_x == -1 and block_y == 0:
                score = block_id
            else:
                if block_id == 3:
                    paddle = block_x
                    frame_done[1] = True
                if block_id == 4:
                    ball = block_x
                    frame_done[0] = True
                grid[(block_x,block_y)] = block_id
        except EndOfCode:
            halt = True
        except IndexError:
            if ball < paddle:
                pc.put(-1)
            elif ball > paddle:
                pc.put(1)
            else:
                pc.put(0)

    print('Part 2 score = {}'.format(score))
