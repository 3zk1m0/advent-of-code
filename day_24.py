from collections import defaultdict

#with open("input.txt") as f:
with open("day_24.txt") as f:
    #grid = defaultdict(lambda: '.')
    grid = {}
    row = 0
    inputs = f.readline().strip()
    while inputs:
        for index, items in enumerate(inputs):
            grid[(index, row)] = items
        inputs = f.readline().strip()
        row += 1






def draw_grid(grid, output_result=False):
    x_bounds = (0, 5)
    y_bounds = (0, 5)
    result = ""
    for y in range(*y_bounds):
        output = ''
        for x in range(*x_bounds):
            output += grid[(x,y)]
        if output_result:
            result += output
        else:
            print(output)
    if output_result:
        return result

def emulate_one(grid, position):
    count = 0
    for dirs in [(1,0),(-1,0),(0,1),(0,-1)]:
        try:
            tmp = grid[position[0]+dirs[0],position[1]+dirs[1]]
        except KeyError:
            tmp = '.'
        if tmp == '#':
            count += 1
    if count == 1 and grid[position] == '#':
        return '#'
    elif count != 1 and grid[position] == '#':
        return '.'
    elif count in [1,2] and grid[position] == '.':
        return '#'
    else:
        return '.'


def emulate_minute(grid):
    grid_copy = grid.copy()
    for pos in grid.keys():
        grid_copy[pos] = emulate_one(grid, pos)
    grid = grid_copy.copy()
    return grid

def find_loop(grid):
    seen = set()
    seen.add(draw_grid(grid, True))
    while True:
        grid = emulate_minute(grid)
        hashed_grid = draw_grid(grid, True)
        if hashed_grid in seen:
            return hashed_grid
        seen.add(hashed_grid)

def part_1():
    loop = find_loop(grid)
    score = 0
    tmp = 1
    for item in loop:
        if item == '#':
            score += tmp
        tmp *= 2
    return score

def get_inner(grid, key, dirs):
    try:
        count = 0
        if (1,0) == dirs:
            for tmp in [(0,i) for i in range(0,5)]:
                if grid[key+1][tmp] == '#':
                    count += 1
        elif (-1,0) == dirs:
            for tmp in [(4,i) for i in range(0,5)]:
                if grid[key+1][tmp] == '#':
                    count += 1
        elif (0,1) == dirs:
            for tmp in [(i,0) for i in range(0,5)]:
                if grid[key+1][tmp] == '#':
                    count += 1
        elif(0,-1) == dirs:
            for tmp in [(i,4) for i in range(0,5)]:
                if grid[key+1][tmp] == '#':
                    count += 1
        return count
    except:
        return 0

def get_outer(grid, key, dirs):
    try:
        if (1,0) == dirs:
            return grid[key-1][(3,2)]
        elif (-1,0) == dirs:
            return grid[key-1][(1,2)]
        elif (0,1) == dirs:
            return grid[key-1][(2,3)]
        elif(0,-1) == dirs:
            return grid[key-1][(2,1)]
        else:
            return '.'
    except:
        return '.'

def emulate_one_recursive(grid, key, position):
    count = 0
    for dirs in [(1,0),(-1,0),(0,1),(0,-1)]:
        try:
            tmp = grid[key][position[0]+dirs[0],position[1]+dirs[1]]
        except KeyError:
            tmp = get_outer(grid, key, dirs)


        if tmp == '#':
            count += 1
        elif tmp == '?':
            count += get_inner(grid, key, dirs)

    if count == 1 and grid[key][position] == '#':
        return '#'
    elif count != 1 and grid[key][position] == '#':
        return '.'
    elif count in [1,2] and grid[key][position] == '.':
        return '#'
    elif grid[key][position] == '?':
        return '?'
    else:
        return '.'

def emulate_minute_recursive(grid):
    grid_copy = grid.copy()
    for keys in grid.keys():
        layer_copy = grid[keys].copy()
        for pos in grid[keys]:
            layer_copy[pos] = emulate_one_recursive(grid, keys, pos)
        grid_copy[keys] = layer_copy.copy()
    grid = grid_copy.copy()
    return grid

def count_all_layers(grid):
    count = 0
    for layer in grid.values():
        for items in layer.keys():
            if layer[items] == '#':
                count += 1
    return count

def part_2():
    grid[(2,2)] = '?'
    grid_empty = grid.copy()
    for keys in grid_empty.keys():
        grid_empty[keys] = '.'
    recursive_grid = {}

    for index in range(-200,200):
        recursive_grid[index] = grid_empty.copy()
        recursive_grid[index][(2,2)] = '?'
    recursive_grid[0] = grid.copy()

    for _ in range(200):
        recursive_grid = emulate_minute_recursive(recursive_grid)


    return count_all_layers(recursive_grid)


if __name__ == "__main__":

    print("Part 1 = {}".format(part_1()))
    print("Part 2 = {}".format(part_2()))


