
with open("day_23.txt") as f:
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

    def run(self, input_data=None, timeout=None):
        if input_data:
            self.put(input_data)
        t = 0
        while (not timeout) or (t < timeout):
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

            if opcode == 1:  # addition
                self.state[params[2]] = self.state[params[0]] + self.state[params[1]]
            elif opcode == 2:  # multiplication
                self.state[params[2]] = self.state[params[0]] * self.state[params[1]]
            elif opcode == 3:  # input
                try:
                    self.state[params[0]] = self.inputs[0]
                    del self.inputs[0]
                except:
                    self.state[params[0]] = -1
            elif opcode == 4:  # output
                self.pointer += 2
                return self.state[params[0]]
            elif opcode == 5:  # jump_if_not
                if self.state[params[0]] != 0:
                    self.pointer = self.state[params[1]]
                    continue
            elif opcode == 6:  # jump_if
                if self.state[params[0]] == 0:
                    self.pointer = self.state[params[1]]
                    continue
            elif opcode == 7:  # smaller
                if self.state[params[0]] < self.state[params[1]]:
                    self.state[params[2]] = 1
                else:
                    self.state[params[2]] = 0
            elif opcode == 8:  # equal
                if self.state[params[0]] == self.state[params[1]]:
                    self.state[params[2]] = 1
                else:
                    self.state[params[2]] = 0
            elif opcode == 9:  # new_rel_base
                self.rel_base += self.state[params[0]]

            t += 1
            self.pointer += STEPS[opcode]

    def put(self, obj):
        self.inputs.append(obj)

def part_1():
    computers = []
    for index in range(50):
        computers.append(IntCode_Computer())
        computers[index].put(index)

    while True:
        for index in range(50):
            address = computers[index].run(timeout=10)
            if not address:
                continue
            x = computers[index].run()
            y = computers[index].run()
            if address == 255:
                return y
            else:
                computers[address].put(x)
                computers[address].put(y)

def part_2():
    computers = []
    NAT = None
    LAST_NAT = None
    for index in range(50):
        computers.append(IntCode_Computer())
        computers[index].put(index)

    timer = 0
    while True:

        if timer > 500:
            computers[0].put(NAT[0])
            computers[0].put(NAT[1])
            if LAST_NAT and NAT[1] == LAST_NAT:
                return LAST_NAT
            LAST_NAT = NAT[1]
            timer = 0

        for index in range(50):
            address = computers[index].run(timeout=10)
            if not address:
                continue
            x = computers[index].run()
            y = computers[index].run()
            if address == 255:
                NAT = [x, y]
            else:
                computers[address].put(x)
                computers[address].put(y)
        timer += 1


if __name__ == "__main__":

    print('Part 1 = {}'.format(part_1()))
    print('Part 2 = {}'.format(part_2()))
