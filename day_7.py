
from itertools import permutations

with open("test.txt") as f:
    inputs = list(map(int, f.readline().strip().split(",")))

STEPS = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}


class EndOfCode(Exception):
    pass


class IntCode_Computer:
    def __init__(self):
        self.state = inputs[:]
        self.pointer = 0
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
                    params.append(self.state[self.state[self.pointer + i]])
                else:
                    params.append(self.state[self.pointer + i])


            if opcode == 1:
                outpos = self.state[self.pointer + 3]
                self.state[outpos] = params[0] + params[1]
            elif opcode == 2:
                outpos = self.state[self.pointer + 3]
                self.state[outpos] = params[0] * params[1]
            elif opcode == 3:
                self.state[self.state[self.pointer + 1]] = self.inputs[0]
                del self.inputs[0]
            elif opcode == 4:
                self.pointer += 2
                return params[0]
            elif opcode == 5:
                if params[0] != 0:
                    self.pointer = params[1]
                    continue
            elif opcode == 6:
                if params[0] == 0:
                    self.pointer = params[1]
                    continue
            elif opcode == 7:
                if params[0] < params[1]:
                    self.state[self.state[self.pointer + 3]] = 1
                else:
                    self.state[self.state[self.pointer + 3]] = 0
            elif opcode == 8:
                if params[0] == params[1]:
                    self.state[self.state[self.pointer + 3]] = 1
                else:
                    self.state[self.state[self.pointer + 3]] = 0

            self.pointer += STEPS[opcode]

    def put(self, obj):
        self.inputs.append(obj)

# Part 1
result = float("-inf")
for config in permutations(range(5)):
    amps = []
    for i in range(len(config)):
        amps.append(IntCode_Computer())
        amps[i].put(config[i])

    s0 = 0
    for i in range(len(config)):
        amps[i].put(s0)
        s0 = amps[i].run()
    if result < s0:
        result = s0
print(result)


# Part 2
result = float("-inf")
for config in permutations(range(5, 10)):
    amps = []
    for i in range(len(config)):
        amps.append(IntCode_Computer())
        amps[i].put(config[i])

    s0 = 0
    halt = False
    while not halt:
        for i in range(len(config)):
            amps[i].put(s0)
            try:
                s0 = amps[i].run()
            except EndOfCode:
                halt = True
    if result < s0:
        result = s0
print(result)