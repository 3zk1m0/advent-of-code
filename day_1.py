


from math import floor

with open("day_1.txt") as f:
    values = f.read().splitlines()
    values = [int(x) for x in values]

def fuel_counter_upper(value):
    return floor(value / 3) - 2

def fuel_counter_for_fuel(value):
    fuel = floor(value / 3) - 2
    if fuel < 0:
        return 0
    return  fuel + fuel_counter_for_fuel(fuel)

if __name__ == "__main__":
    the_sum_modules = 0
    the_sum_all = 0
    for value in values:
        the_sum_modules += fuel_counter_upper(value)
        the_sum_all += fuel_counter_for_fuel(value)

    print('only modules: {}'.format(the_sum_modules))
    print('modules and fuel: {}'.format(the_sum_all))