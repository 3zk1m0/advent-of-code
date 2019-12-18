
# Thanks for help https://repl.it/@joningram/AOC-2019   reddit: u/i_have_no_biscuits

from itertools import permutations

with open("day_18.txt") as f:
    the_data = f.readline().strip()
    grid = {}
    row = 0
    keys = {}
    doors = {}
    while the_data:
        for index, items in enumerate(the_data):
            grid[(index,row)] = items
            if items.isupper():
                doors[items] = (index,row)
            if items.islower():
                keys[items] = (index,row)
            if items == '@':
                location = [index,row]
        row += 1
        the_data = f.readline().strip()

def draw_grid(grid):

    x_bounds = (min(p[0] for p in grid), max(p[0] for p in grid) + 1, 1)
    y_bounds = (max(p[1] for p in grid), min(p[1] for p in grid) - 1, -1)
    
    for y in range(*y_bounds)[::-1]:
        output = ''
        for x in range(*x_bounds):
            output += grid[(x,y)]
        print(output)
        
def distances_from(grid, start):
    start_x, start_y = start
    visited = set([(start_x, start_y)])
    queue = [(start_x, start_y, 0, "")]
    routeinfo = {}

    for (x, y, distance, route) in queue:
        value = grid[(x,y)]
        if value not in ".@#1234" and distance > 0:
            routeinfo[value] = (distance, route)
            route = route + value
        visited.add((x,y))

        for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
            new_x, new_y = x + direction[0], y + direction[1]
            if grid[(new_x, new_y)] != '#' and (new_x, new_y) not in visited:
                queue.append((new_x, new_y, distance + 1, route))
    return routeinfo

def find_routeinfo(grid, part2=False):
    routeinfo = {}
    for items in keys.keys():
        routeinfo[items] = distances_from(grid, keys[items])
    if part2:
        for item in "1234":
            index = list(grid.keys())[list(grid.values()).index(item)]
            routeinfo[item] = distances_from(grid, index)
    else:
        routeinfo['@'] = distances_from(grid, location)
    return routeinfo

def part_1():
    routeinfo = find_routeinfo(grid)
    all_keys = frozenset(key for key in keys.keys())
    info = {('@',frozenset()):0}

    for _ in keys:
        next_info = {}
        for item in info:
            current_location = item[0]
            current_keys = item[1]
            current_distance = info[item]
            for new_key in all_keys:
                if new_key not in current_keys:
                    distance, route = routeinfo[current_location][new_key]
                    reachable = all((char.lower() in current_keys) for char in route)

                    if reachable:
                        new_distance = current_distance + distance
                        new_keys = frozenset(current_keys | set((new_key,)))

                        if (new_key, new_keys) not in next_info or new_distance < next_info[(new_key, new_keys)]:
                            next_info[(new_key, new_keys)] = new_distance
        info = next_info
    
    return min(info.values())

def part_2():
    for direction in [(0,0),(1,0),(0,1),(-1,0),(0,-1)]:
        grid[(location[0]+direction[0], location[1]+direction[1])] = '#'
    for index, direction in enumerate([(-1,-1),(-1,1),(1,-1),(1,1)]):
        grid[(location[0]+direction[0], location[1]+direction[1])] = str(index+1)

    routeinfo = find_routeinfo(grid, True)
    all_keys = frozenset(key for key in keys.keys())
    info = {(('1','2','3','4'),frozenset()):0}

    for _ in keys:
        next_info = {}
        for item in info:
            current_location = item[0]
            current_keys = item[1]
            current_distance = info[item]

            for new_key in all_keys:
                if new_key not in current_keys:
                    for robot in range(4):
                        if new_key in routeinfo[current_location[robot]]:
                            distance, route = routeinfo[current_location[robot]][new_key]
                            reachable = all((char.lower() in current_keys) for char in route)
                            
                            if reachable:
                                new_distance = current_distance + distance
                                new_keys = frozenset(current_keys | set((new_key,)))
                                new_location = list(current_location)
                                new_location[robot] = new_key
                                new_location = tuple(new_location)

                                if (new_location, new_keys) not in next_info or new_distance < next_info[(new_location, new_keys)]:
                                    next_info[(new_location, new_keys)] = new_distance
        info = next_info

    return min(info.values())


if __name__ == "__main__":

    print('Part 1 = {}'.format(part_1()))
    print('Part 2 = {}'.format(part_2()))











