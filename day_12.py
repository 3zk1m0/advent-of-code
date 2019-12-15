
import math

the_data = [
    [14,15,-2],
    [17,-3,4],
    [6,12,-13],
    [-2,10,-8],
]

DEBUG = False

def calculate_velocity_for_moon(moon, other, old_velocity):
    velocity = old_velocity.copy()
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

def part_1():
    total_energy = 0
    moons = [
    [14,15,-2],
    [17,-3,4],
    [6,12,-13],
    [-2,10,-8],
    ]
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
    return total_energy

def part_2():
    moons = [
    [14,15,-2],
    [17,-3,4],
    [6,12,-13],
    [-2,10,-8],
    ]
    moons_velocity = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    ]

    seen_x = set()
    rep_x = None
    seen_y = set()
    rep_y = None
    seen_z = set()
    rep_z = None

    for i in range(1000000):
        if rep_x and rep_y and rep_z:
            break

        for index, moon in enumerate(moons):
            moons_velocity[index] = calculate_velocity_for_moon(moon, moons[:index]+moons[index+1:], moons_velocity[index])

        for index, moon in enumerate(moons):
            moons[index] = apply_velocity(moon, moons_velocity[index])

        if not rep_x:
            xk = str([[moons[index][0], moons_velocity[index][0]] for index in range(len(moons))])
            if xk in seen_x:
                rep_x = i
            seen_x.add(xk)
        if not rep_y:
            yk = str([[moons[index][1], moons_velocity[index][1]] for index in range(len(moons))])
            if yk in seen_y:
                rep_y = i
            seen_y.add(yk)
        if not rep_z:
            zk = str([[moons[index][2], moons_velocity[index][2]] for index in range(len(moons))])
            if zk in seen_z:
                rep_z = i
            seen_z.add(zk)

    
    def lcm(x, y):
        return x // math.gcd(x, y) * y

    return lcm(lcm(rep_x, rep_y), rep_z)


if __name__ == "__main__":
    
    print(part_1())
    print(part_2())
   