
with open("day_25.txt") as f:
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
                    input_data = input("Input: ")
                    for letter in input_data:
                        self.put(ord(letter))
                    self.put(10)
                    self.state[params[0]] = self.inputs[0]
                    del self.inputs[0]
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

    commands = [
        "south\n",
        "south\n",
        "west\n",
        "north\n"
        "north\n",
        "take tambourine\n",
        "south\n",
        "south\n",
        "east\n",
        "south\n",
        "west\n",
        #"take asterisk\n",
        "east\n",
        "take fixed point\n",
        "south\n",
        #"take festive hat\n",
        "west\n",
        "west\n",
        #"take jam\n",
        "south\n",
        "take easter egg\n",
        "north\n",
        "east\n",
        "east\n",
        "north\n",
        "north\n",
        "north\n",
        "west\n",
        "south\n",
        #"take antenna\n",
        "north\n",
        "west\n",
        "west\n",
        "take space heater\n",
        "west\n",
        "west\n"
    ]
    # 'space heater', 'easter egg', 'fixed point', 'tambourine'
    pc = IntCode_Computer()
    for items in commands:
        for letters in items:
            pc.put(ord(letters))

    halted = False
    while not halted:
        try:
            output = pc.run()
            print(chr(output), end="")
        except EndOfCode:
            halted = True




if __name__ == "__main__":

    part_1()

