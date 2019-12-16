
with open("day_16.txt") as f:
    the_data = f.readline().strip()


repeat_pattern = [0, 1, 0, -1]

def calculate_row(input_data, times):
    input_data = [number for number in input_data]
    pattern = []
    while len(pattern)-1 < len(input_data):
        for item in repeat_pattern:
            pattern += [item]*times
    del pattern[0]

    total = sum([int(input_data[index]) * int(pattern[index]) for index in range(len(input_data))])

    return str(total)[-1]

def calculate_phase(input_data):
    output = ""
    for index in range(1, len(input_data)+1):
        output += calculate_row(input_data, index)
    return output

def part_1():
    input_data = the_data[:]
    for _ in range(100):
        input_data = calculate_phase(input_data)
    return input_data[:8]

def part_2():
    offset = int(the_data[:7])
    input_data = list(map(int, the_data[:] * 10000))
    input_length = len(input_data)
    
    if input_length > offset*2:
        return "Not working"

    for _ in range(100):
        tmp_sum = sum(input_data[index] for index in range(offset, input_length))
        for index in range(offset, input_length):
            tmp = int(str(tmp_sum)[-1])
            tmp_sum -= input_data[index]
            input_data[index] = tmp

    return ''.join(map(str, input_data[offset: offset+8]))


if __name__ == "__main__":
    print('Part 1 = {}'.format(part_1()))
    print('Part 2 = {}'.format(part_2()))
