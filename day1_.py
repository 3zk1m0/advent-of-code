values = [
110321,
61817,
107271,
126609,
84016,
119187,
53199,
117553,
83163,
69434,
62734,
76774,
75016,
126859,
114626,
70782,
102903,
105871,
108500,
149367,
99266,
131731,
86778,
110561,
116521,
138216,
55347,
135516,
126801,
124902,
103083,
130858,
54885,
126837,
71103,
143975,
135207,
77264,
149331,
85252,
78910,
84007,
123953,
87355,
113433,
57750,
78394,
106081,
110942,
118180,
71745,
60080,
56637,
105491,
111329,
71799,
59962,
60597,
75241,
102506,
75341,
129539,
71011,
127185,
51245,
144401,
78592,
116835,
52029,
134905,
80104,
146304,
113780,
108124,
131268,
124765,
78847,
76897,
56445,
116487,
62068,
125176,
122259,
134261,
101127,
127089,
55793,
113113,
132835,
118901,
59574,
113399,
73232,
93720,
144450,
129604,
101741,
108759,
55891,
52939]

from math import floor


"""
Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
"""
def fuel_counter_upper(value):
    return floor(value / 3) - 2

"""
Fuel itself requires fuel just like a module - take its mass, divide by three, round down,
and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on.
Any mass that would require negative fuel should instead be treated as if it requires zero fuel;
the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.
"""
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