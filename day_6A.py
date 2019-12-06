

with open('day_6.txt', 'r') as f:
    the_data = f.read().splitlines()

test_data = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L']

def parse_data(data):
    result = []
    for items in data:
        result.append(items.split(')'))

    return result

def find_com(data):
    for index, item in enumerate(data):
        if item[0] == 'COM':
            return index
    return -1

def find_next(data, to_find):
    for items in data:
        if items[0] == to_find:
            return items[1]
    return -1

def find_parrent(data, to_find):
    for items in data:
        if items[1] == to_find:
            return items[0]
    return -1

def remove_last(data, to_find):
    for index, item in enumerate(data):
        if item[1] == to_find:
            del data[index]

def count_to_root(data, pos):
    result = 0
    last_pos = pos
    while True:
        if last_pos == 'COM':
            return result
        last_pos = find_parrent(data, last_pos)
        result += 1

def find_last_child(data):
    done = False
    last_pos = 'COM'
    while not done:
        next_pos = find_next(data, last_pos)
        if next_pos == -1:
            return last_pos
        else:
            last_pos = next_pos


if __name__ == "__main__":
    
    data = parse_data(the_data)

    count = 0
    while data:
        last_child = find_last_child(data)
        count += count_to_root(data, last_child)
        remove_last(data, last_child)

    print(count)


