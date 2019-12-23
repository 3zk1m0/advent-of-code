
from collections import defaultdict

#with open("test.txt") as f:
with open("day_20.txt") as f:
    the_data = f.readline()[:-1]
    grid = defaultdict(lambda:' ')
    row = 0
    while the_data:
        for index, items in enumerate(the_data):
            grid[(index,row)] = items
        row += 1
        the_data = f.readline()[:-1]


def draw_grid(grid):

    x_bounds = (min(p[0] for p in grid), max(p[0] for p in grid) + 1, 1)
    y_bounds = (max(p[1] for p in grid), min(p[1] for p in grid) - 1, -1)
    
    for y in range(*y_bounds)[::-1]:
        output = ''
        for x in range(*x_bounds):
            output += grid[(x,y)]
        print(output)

def get_portal(grid, letter):
    letter_1 = letter[1]
    letter_1_pos = letter[0]
    portal = None
    for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
        new_pos = (letter_1_pos[0]+direction[0],letter_1_pos[1]+direction[1])
        if grid[new_pos].isalpha():
            letter_2 = grid[new_pos]
            letter_2_pos = new_pos
        if grid[new_pos] == '.':
            portal = new_pos
            
    if not portal:
        for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
            new_pos = (letter_2_pos[0]+direction[0],letter_2_pos[1]+direction[1])
            if grid[new_pos] == '.':
                portal = new_pos



    if letter_1_pos[0] != letter_2_pos[0]:
        if letter_1_pos[0] < letter_2_pos[0]:
            return [letter_1+letter_2, portal]
        else:
            return [letter_2+letter_1, portal]
    else:
        if letter_1_pos[1] < letter_2_pos[1]:
            return [letter_1+letter_2, portal]
        else:
            return [letter_2+letter_1, portal]

def get_all_portals(grid):
    portals = {}
    seen = set()
    x_bounds = (min(p[0] for p in grid), max(p[0] for p in grid) + 1)
    y_bounds = (min(p[1] for p in grid), max(p[1] for p in grid) + 1)

    x_outer = (x_bounds[1] * 0.1, x_bounds[1] * 0.9)
    y_outer = (y_bounds[1] * 0.1, y_bounds[1] * 0.9)
    for items in list(grid.items()):
        if items[1].isalpha():
            tmp = get_portal(grid, items)
            if tmp[1] not in seen:
                seen.add(tmp[1])
                x_result = tmp[1][0] < x_outer[0] or tmp[1][0] > x_outer[1]
                y_result = tmp[1][1] < y_outer[0] or tmp[1][1] > y_outer[1]
                if x_result or y_result:
                    if tmp[0] in portals:
                        portals[tmp[0]][0] = tmp[1]
                    else:
                        portals[tmp[0]] = [tmp[1],None]
                else:
                    if tmp[0] in portals:
                        portals[tmp[0]][1] = tmp[1]
                    else:
                        portals[tmp[0]] = [None,tmp[1]]
    return portals, seen

def part_1(grid, portals):
    grid_copy = grid.copy()
    steps = 0
    start = portals["AA"][0]
    end = portals["ZZ"][0]
    del portals["AA"]
    del portals["ZZ"]
    grid_copy[start] = '%'
    while grid_copy[end] == '.':
        #draw_grid(grid_copy)
        steps += 1
        tmp = [key for key in grid_copy.keys() if grid_copy[key] == '%']

        for portal in portals.values():
            if grid_copy[portal[0]] == '%':
                    grid_copy[portal[0]] = '&'
                    grid_copy[portal[1]] = '%'
            elif grid_copy[portal[1]] == '%':
                    grid_copy[portal[1]] = '&'
                    grid_copy[portal[0]] = '%'

        if not tmp:
            return  -1
        for items in tmp:
            for dirs in [(-1,0),(0,1),(1,0),(0,-1)]:
                if grid_copy[(items[0]+dirs[0],items[1]+dirs[1])] == '.':
                    grid_copy[(items[0]+dirs[0],items[1]+dirs[1])] = '%'
            grid_copy[items] = '&'

    return steps

def part_2(grid, portals):
    recursion_limit = 20
    layers = [grid.copy()]
    steps = 0
    start = portals["AA"][0]
    end = portals["ZZ"][0]
    del portals["AA"]
    del portals["ZZ"]
    layers[0][start] = '%'
    while layers[0][end] == '.':
        steps += 1
        for index, _ in enumerate(layers):
            tmp_layers = layers.copy()
            tmp = [key for key in layers[index].keys() if layers[index][key] == '%']

            for portal in portals.values():
                if layers[index][portal[1]] == '%' and index < recursion_limit:
                    try:
                        tmp_layers[index+1]
                    except:
                        tmp_layers.append(grid.copy())
                    tmp_layers[index][portal[1]] = '&'
                    tmp_layers[index+1][portal[0]] = '%'
                elif layers[index][portal[0]] == '%' and index != 0:
                        tmp_layers[index][portal[0]] = '&'
                        tmp_layers[index-1][portal[1]] = '%'

            # ei laske portaali askeleita
            for items in tmp:
                for dirs in [(-1,0),(0,1),(1,0),(0,-1)]:
                    if layers[index][(items[0]+dirs[0],items[1]+dirs[1])] == '.':
                        tmp_layers[index][(items[0]+dirs[0],items[1]+dirs[1])] = '%'
                tmp_layers[index][items] = '&'
            
            layers = tmp_layers.copy()
    
    return steps

if __name__ == "__main__":

    start = "AA"
    end = "ZZ"

    #draw_grid(grid)
    portals, seen = get_all_portals(grid)
    #print(part_1(grid, portals))
    print(part_2(grid, portals))


