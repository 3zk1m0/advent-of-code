
the_data = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,19,5,23,2,6,23,27,1,6,27,31,2,31,9,35,1,35,6,39,1,10,39,43,2,9,43,47,1,5,47,51,2,51,6,55,1,5,55,59,2,13,59,63,1,63,5,67,2,67,13,71,1,71,9,75,1,75,6,79,2,79,6,83,1,83,5,87,2,87,9,91,2,9,91,95,1,5,95,99,2,99,13,103,1,103,5,107,1,2,107,111,1,111,5,0,99,2,14,0,0]



def operate(data, pointer):
    operator = data[pointer]
    if operator == 1:
        value1 = data[data[pointer+1]]
        value2 = data[data[pointer+2]]
        data[data[pointer+3]] = value1 + value2
    elif operator == 2:
        value1 = data[data[pointer + 1]]
        value2 = data[data[pointer + 2]]
        data[data[pointer + 3]] = value1 * value2
    elif operator == 99:
        return False

    return True


if __name__ == "__main__":

    the_data[1] = 12
    the_data[2] = 2

    for noun in range(100):
        for verb in range(100):
            test_data = list(the_data)
            running = True
            pointer = 0
            test_data[1] = noun
            test_data[2] = verb
            while running:
                running = operate(test_data, pointer)
                pointer += 4

            if test_data[0] == 19690720:
                print('{} - {}'.format(noun, verb))
                print(100 * noun + verb)
