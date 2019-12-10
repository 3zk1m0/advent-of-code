
from math import atan2, degrees, hypot, pi

with open("day_10.txt") as f:
    line = f.readline().strip()
    lines = [line]
    while line:
        line = f.readline().strip()
        lines.append(line)

#for items in lines:
 #   print(items)

asteroids = []

for index_y, row in enumerate(lines):
    for index_x, value in enumerate(row):
        if value == '#':
            asteroids.append([index_x, index_y, []])

def get_angle(x,y):
    return atan2(y[0] - x[0], x[1] - y[1]) % (2 * pi)

def dist(x, y):
    return hypot(x[0]-y[0], x[1]-y[1])


for index, origins in enumerate(asteroids):
    for other in asteroids[:index]+asteroids[index+1:]:
        angle = get_angle(origins, other)
        if angle not in asteroids[index][2]:
            asteroids[index][2].append(angle)

the_index = 0
largest = 0
coordinates = [0,0]
for index, items in enumerate(asteroids):
    if len(items[2]) > largest:
        largest = len(items[2])
        the_index = index
        coordinates = [items[0],items[1]]

print('Part 1 = {} - {}'.format(largest, coordinates))



tmp = []
for items in asteroids:
        tmp.append([items[0],items[1]])
asteroids = tmp
asteroids.remove(coordinates)

asteroids.sort(key=lambda item: dist(item, coordinates))

ranks = {}
for index, item in enumerate(asteroids):
    rank = 0
    for items in asteroids[:index]:
        if get_angle(coordinates, item) == get_angle(coordinates, items):
            rank += 1
    ranks[str(item)] = rank

result = sorted(asteroids, key=lambda b: (ranks[str(b)], get_angle(coordinates, b)))[199]
print('Part 2 = {}'.format(result[0] * 100 + result[1]))












quit()
station = [coordinates[0], coordinates[1], []]
for other in asteroids:
    angle = get_angle(station, other)
    distance = dist(station, other)
    if distance != 0:
        station[2].append([angle, other[0], other[1], distance])


station[2] = sorted(station[2], key=lambda x: x[3])
station[2] = sorted(station[2], key=lambda x: x[0])



offset = 180

index = 0
found = 0
for items in station[2]:
    if items[0] == offset:
        found = index
        break
    index += 1

station[2] = station[2][found:]+station[2][:found]

#print(station)

count = 0
last_degree = offset-1
asteroids = station[2]
while True:
    for index, items in enumerate(asteroids):
        
        if items[0] != last_degree:
            count += 1
            print(items)
                    #if count == 200:
            if items[1] == 4 and items[2] == 4:
                print(count)
                print(items[1]*100+items[2])
                quit()
            del asteroids[index]
        else:
            print('skiped - {}'.format(items))
        last_degree = items[0]


    