# ___________________________ Dependencies ___________________________
import sys

# ___________________________ Base dictionaries ___________________________
###
# dictionaries keep all values and how to convert them to 'base'
# example: cm to m, km to m, lbs to g, kg to g
# then base result converted to desired units (no need for if-else/choice hell)
###
length_units = {
    'pm': 0.000000000001,
    'nm': 0.000000001,
    'um': 0.000001,
    'mm': 0.001,
    'cm': 0.01,
    'm': 1, # base
    'km': 1000,
    'inch': 0.0254,
    'ft': 0.3048,
    'yard': 0.9144,
    'mile': 1609.344
}

weight_units = {
    'pg': 0.000000000001,
    'ng': 0.000000001,
    'ug': 0.000001,
    'mg': 0.001,
    'g': 1, # base
    'kg': 1000,
    'tonne': 1000000,
    'oz': 28.34952,
    'lbs': 453.5924
}

speed_units = {
    'cm/s': 0.01,
    'm/s': 1, # base
    'm/min': 0.0166666667,
    'km/s': 1000,
    'km/min': 16.666666667,
    'km/h': 0.2777778,
    'ips': 0.0254,
    'fps': 0.3048,
    'mph': 0.44704,
    'knot': 0.5144447
}

time_units = {
    'ps': 0.000000000001,
    'ns': 0.000000001,
    'us': 0.000001,
    'ms': 0.001,
    's': 1, # base
    'min': 60,
    'h': 3600,
    'day': 86400,
    'week': 604800,
    'month': 2629800,
    'year': 31557600
}

to_celsius = {
    'c': lambda x: x, # base
    'k': lambda x: x - 273.15,
    'f': lambda x: x - 32 * (5/9)
}

from_celsius = {
    'c': lambda x: x, # base
    'k': lambda x: x + 273.15,
    'f': lambda x: x * (9/5) + 32
}

timezones = {
    'utc-11': -11,
    'utc-10': -10,
    'utc-9': -9,
    'utc-8': -8,
    'utc-7': -7,
    'utc-6': -6,
    'utc-5': -5,
    'utc-4': -4,
    'utc-3': -3,
    'utc-2': -2,
    'utc-1': -1,
    'utc+0': 0, # base
    'utc+1': 1,
    'utc+2': 2,
    'utc+3': 3,
    'utc+4': 4,
    'utc+5': 5,
    'utc+6': 6,
    'utc+7': 7,
    'utc+8': 8,
    'utc+9': 9,
    'utc+10': 10,
    'utc+11': 11,
    'utc+12': 12
}

# ___________________________ Read CLI data ___________________________
###
# get data from CLI
# example: > convert.py 12 cm m -> [12, 'cm', 'm']
###
argv = sys.argv[1:]
if len(argv) != 3:
    print('Wrong input, example - python convert.py 12 cm m\n')
    print('P.S. use singular unit name - inch not inches')
    sys.exit()
argv = [x.lower() for x in argv]
value = argv[0]
source = argv[1]
target = argv[2]

# ___________________________ Simple conversionts ___________________________
###
# 1) convert units to base (multiply value by dictionary value)
# 2) divide result from desired units dictionary value
# example: 12 cm km -> 12 * 0.01 (cm:0.01) -> 0.12 / 1000 (km:1000) -> 0.00012 km
###
# --------------- weight, length, speed, time
def simple_convert(val, src, target): 
    for unit_dict in [length_units, weight_units, speed_units, time_units]:
        if src in unit_dict:
            val = float(val)
            result = val * unit_dict[src] / unit_dict[target]
            print(f'{val}{src} = {round(result, 2)}{target}')
            break

# ___________________________ Temperature conversion ___________________________
def temp_convert(val, src, target):
###
# 1) convert temperature to Celsius
# 2) convert Celsius to desired units
# example: 12 C K -> 12 (celsius is base, - if other) -> 12 + 273.15 -> 285.15
###
    val = float(val)
    celsius = to_celsius[src](val) 
    result = from_celsius[target](celsius)
    # temperature units written in capital letters
    src = src.capitalize()
    target = target.capitalize()
    print(f'{val}{src} = {result}{target}')

# ___________________________ Time zone conversion ___________________________
def time_zone_convert(val, src, target):
###
# 1) convert everything to UTC (example: EDT+6 -> UTC+6)
# 2) convert to UTC+0 (by subtracting number after letters)
# 3) convert to desired displacement (add number after letters)
# example: 4:30 EDT-2 GMT+4.30
# 4:30 EDT-2 -> 4:30 UTC-2 -> 6:30 UTC+0 -> 11:00 UTC+4.30
###
    # convert back to capital 
    return

# ___________________________ Choose conversion ___________________________
###
# run 'if' check to choose function based on input
# if source and target units match dictionary keys, run function based on dictionary
# both target and source need to be from same dictionary to work
###
conversions = [
    (length_units, simple_convert),
    (weight_units, simple_convert),
    (speed_units, simple_convert),
    (time_units, simple_convert),
    (to_celsius, temp_convert),
    (timezones, time_zone_convert)
]

for unit_dict, conversion_type in conversions:
    if source in unit_dict and target in unit_dict:
        conversion_type(value, source, target)
        break
# else statement to 'for' not to 'if' (if 'for' loop finishes without calling 'break' (if statement is wrong) - execute 'else')
else:
    print(f'Cannot convert {source} to {target}')
    print("Possible conversions:")
    print(", ".join(length_units.keys()))
    print(", ".join(weight_units.keys()))
    print(", ".join(time_units.keys()))
    print(", ".join(speed_units.keys()))
    print(", ".join(to_celsius.keys()))
    print(", ".join(timezones.keys()))