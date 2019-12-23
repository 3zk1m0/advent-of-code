from itertools import permutations
from collections import defaultdict, deque

with open("day_23.txt") as f:
    inputs = list(map(int, f.readline().strip().split(",")))


STEPS = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}

class EndOfCode(Exception):
    pass


class IntCode_Computer:
    def __init__(self, input):
        self.state = inputs[:]
        self.state += [0] * 10000
        self.pointer = 0
        self.rel_base = 0
        self.inputs = []
        self.input = input

    def run(self, input_data=None, timeout=None):
        if input_data:
            self.put(input_data)
        
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

        t = 0
        while (not timeout) or (t<timeout):
            if opcode == 1: # addition
                self.state[params[2]] = self.state[params[0]] + self.state[params[1]]
            elif opcode == 2: # multiplication
                self.state[params[2]] = self.state[params[0]] * self.state[params[1]]
            elif opcode == 3: # input
                inp = self.input()
                self.state[params[0]] = inp
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

            t += 1
            self.pointer += STEPS[opcode]

    def put(self, obj):
        self.inputs.append(obj)


N = 50
Q = [deque([i]) for i in range(N)]
def get_input(i):
    if Q[i]:
        return Q[i].popleft()
    return -1



if __name__ == "__main__":
    
    computers = []
    computer_memory = []
    for index in range(50):
        computers.append(IntCode_Computer(lambda: get_input(index)))
        computers[index].put(index)

    address = 0

    while True:
        for index in range(50):
            print(index)
            address = computers[index].run(timeout=10)
            if address == None:
                continue
            x = computers[index].run()
            y = computers[index].run()
            if address == 255:
                print(x)
                print(y)
                quit()
            else:
                print('{} - {} {}'.format(address, x, y))
                Q[address].append(x)
                Q[address].append(y)
    





