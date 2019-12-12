# rework
import math

the_data = [
    [14,15,-2],
    [17,-3,4],
    [6,12,-13],
    [-2,10,-8],
]
test_data = [
    [-1,0,2],
    [2,-10,-7],
    [4,-8,8],
    [3,5,-1],
]

DEBUG = False

def calculate_velocity_for_moon(moon, other, old_velocity):
    velocity = old_velocity[:]
    for other_moon in other:
        for index, axis in enumerate(other_moon):
            if moon[index] > axis:
                velocity[index] -= 1
            elif moon[index] < axis:
                velocity[index] +=1

    return velocity

def apply_velocity(moon, velocity):
    moon[0] += velocity[0]
    moon[1] += velocity[1]
    moon[2] += velocity[2]
    return moon

def calculate_energy(potential, kinectic):
    potential_sum = 0
    kinectic_sum = 0
    for index in range(3):
        potential_sum += abs(potential[index])
        kinectic_sum += abs(kinectic[index])
    return potential_sum * kinectic_sum

def debug_print(time, moons, moons_velocity, debug=True):
    if debug:
        print('After {} steps:'.format(time+1))
        for index, moon in enumerate(moons):
            print('pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>'.format(moon[0],moon[1],moon[2], moons_velocity[index][0],moons_velocity[index][1],moons_velocity[index][2]))
        print('')

if __name__ == "__main__":

    total_energy = 0
    moons = the_data[:]
    moons_velocity = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    ]

    debug_print(-1, moons, moons_velocity, DEBUG)
    for times in range(1000):

        for index, moon in enumerate(moons):
            moons_velocity[index] = calculate_velocity_for_moon(moon, moons[:index]+moons[index+1:], moons_velocity[index])

        for index, moon in enumerate(moons):
            moons[index] = apply_velocity(moon, moons_velocity[index])

        debug_print(times, moons, moons_velocity, DEBUG)

    for index, moon in enumerate(moons):
        total_energy += calculate_energy(moon, moons_velocity[index])
    print('Part 1 Total energy = {}'.format(total_energy))


    moons = the_data[:]
    moons_velocity = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    ]

    seenx = set()
    repx = None
    seeny = set()
    repy = None
    seenz = set()
    repz = None
    for i in range(10):
        if repx and repy and repz:
            break


        for index, moon in enumerate(moons):
            moons_velocity[index] = calculate_velocity_for_moon(moon, moons[:index]+moons[index+1:], moons_velocity[index])

        for index, moon in enumerate(moons):
            moons[index] = apply_velocity(moon, moons_velocity[index])


        if not repx:
            xk = str([[moons[index][0], moons_velocity[index][0]] for index in range(len(moons)-1)])
            if xk in seenx:
                repx = i
            seenx.add(xk)
            print(xk)
        if not repy:
            yk = str([[moons[index][1], moons_velocity[index][1]] for index in range(len(moons)-1)])
            if yk in seeny:
                repy = i
            seeny.add(yk)
        if not repz:
            zk = str([[moons[index][2], moons_velocity[index][2]] for index in range(len(moons)-1)])
            if zk in seenz:
                repz = i
            seenz.add(zk)
    print(repx, repy, repz)

    quit()
    def lcm(x, y):
        return x // math.gcd(x, y) * y

    print(lcm(lcm(repx, repy), repz))