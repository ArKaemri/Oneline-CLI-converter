# ___________________________ Dependencies ___________________________
import sys
import re
# ___________________________ Simple dictionaries ___________________________
###
# dictionaries keep all values and how to convert them to 'base'
# example: cm to m, km to m, lbs to g, kg to g
# then base result converted to desired units
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
    'ton': 1000000,
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
    'f': lambda x: (x - 32) * (5/9)
}

from_celsius = {
    'c': lambda x: x, # base
    'k': lambda x: x + 273.15,
    'f': lambda x: x * (9/5) + 32
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
# --------------- weight, length, speed, time
def simple_convert(val, src, target): 
###
# 1) convert units to base (multiply value by dictionary value)
# 2) divide result from desired units dictionary value
# example: 12 cm km -> 12 * 0.01 (cm:0.01) -> 0.12 / 1000 (km:1000) -> 0.00012 km
###
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
    src = src.upper()
    target = target.upper()
    print(f'{val}{src} = {round(result, 2)}{target}')

# ___________________________ Time zone conversion ___________________________
def time_zone_convert(val, src, target):
###
# 1) divide input into 3 parts (symbolic - UTC or EST etc., symbol - +/-, amount - 3 or 4:30 etc.)
# 2) convert amount's and value to time using manual methods
# 3) from value subtract source amount and add target amount
# 4) output starting symbolic (upper before outputing) + result time 
###
    def parse_timezone(data):
        # get values from timezone input
        list = re.match(r'^([a-z]{2,4})([+-])(\d{1,2})(?::(\d{2}))?$', data)
        label = data.upper() # first letters
        sign = list.group(2) # -/+
        hours = int(list.group(3)) # numbers before ':'
        minutes = int(list.group(4) or 0) # numbers after ':' if exist
        offset = hours * 60 + minutes
        if sign == '-':
            offset = -offset
        return label, offset
        
    val_h, val_min = map(int, val.split(':'))
    offset = val_h * 60 + val_min
    src_label, src_offset = parse_timezone(src)
    target_label, target_offset = parse_timezone(target)
    
    total_offset_min = offset - src_offset + target_offset
    # wrap in 24 hours
    total_offset_min %= 24 * 60
    
    result_h = total_offset_min // 60
    result_min = total_offset_min % 60
    print(f'{val_h:02}:{val_min} {src_label} = {result_h:02}:{result_min:02} {target_label}')

# ___________________________ Regex conversion handling ___________________________
###
# used for 1 to 1 conversions, like binary <-> number, or time-zones
# keep dictionary with regex patterns for keys and what function they need for conversion instead normal values
# call function directly based on key
###
# matches
timezone_regex = r'^[a-z]{2,4}[+-]\d{1,2}(:\d{2})?$'

# regex pattern dictionary
regex_dict = {
    re.compile(timezone_regex): time_zone_convert
}

def choose_regex_convert(val, src, target):
    for pattern, func in regex_dict.items():
        if re.match(pattern, src) and re.match(pattern, target):
            func(val, src, target)

# ___________________________ Choose conversion ___________________________
###
# run 'if' check to choose function based on input
# if source and target units match dictionary keys, run function based on dictionary
# both target and source need to be from same dictionary to work
###
conversions = [
    ('simple', length_units, simple_convert),
    ('simple', weight_units, simple_convert),
    ('simple', speed_units, simple_convert),
    ('simple', time_units, simple_convert),
    ('simple', to_celsius, temp_convert),
    ('regex', regex_dict, choose_regex_convert)
]

for kind, unit_dict, conversion_type in conversions:
    if kind == 'simple':
        if source in unit_dict and target in unit_dict:
            conversion_type(value, source, target)
            break
    elif kind == 'regex':
        conversion_type(value, source, target)
        break
# else statement to 'for' not to 'if' (if 'for' loop finishes without calling 'break' (if statement is wrong) - execute 'else')
else:
    print(f'Cannot convert {source} to {target}')
    print('Possible conversions:')
    print('Length: ' + ', '.join(length_units))
    print('Weight: ' + ', '.join(weight_units))
    print('Time: ' + ', '.join(time_units))
    print('Speed: ' + ', '.join(speed_units))
    temp_visual = [key.upper() for key, _ in to_celsius.items()]
    print('Temperature: ' + ', '.join(temp_visual))
    print('Timezones: ***-11 to ***+12')