# ___________________________ Dependencies ___________________________
import sys
import re
# ___________________________ Simple dictionaries ___________________________
###
# dictionaries keep all values and how to convert them to 'base'
# example: cm to m, kilometer to meter, lbs to gram, kg to g
# then base result converted to desired units
# P.S. - key can be a tuple to accept full name or shortened (m or meter) OR multiple same value objects (timezones)
###
length_units = {
    ('pm', 'picometer'): 0.000000000001,
    ('nm', 'nanometer'): 0.000000001,
    ('um', 'micrometer'): 0.000001,
    ('mm', 'millimeter'): 0.001,
    ('cm', 'centimeter'): 0.01,
    ('m', 'meter'): 1, # base
    ('km', 'kilometer'): 1000,
    'inch': 0.0254,
    ('ft', 'feet'): 0.3048,
    'yard': 0.9144,
    'mile': 1609.344
}

weight_units = {
    ('pg', 'picogram'): 0.000000000001,
    ('ng', 'nanogram'): 0.000000001,
    ('ug', 'microgram'): 0.000001,
    ('mg', 'miligram'): 0.001,
    ('g', 'gram'): 1, # base
    ('kg', 'kilogram'): 1000,
    'ton': 1000000,
    ('oz', 'ounce'): 28.34952,
    ('lbs', 'pound'): 453.5924
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
    ('ps', 'picosecond'): 0.000000000001,
    ('ns', 'nanosecond'): 0.000000001,
    ('us', 'microsecond'): 0.000001,
    ('ms', 'millisecond'): 0.001,
    ('s', 'second'): 1, # base
    ('min', 'minute'): 60,
    ('h', 'hour'): 3600,
    'day': 86400,
    'week': 604800,
    'month': 2629800,
    'year': 31557600
}

to_celsius = {
    ('c', 'celsius'): lambda x: x, # base
    ('k', 'kelvin'): lambda x: x - 273.15,
    ('f', 'fahrenheit'): lambda x: (x - 32) * (5/9)
}

from_celsius = {
    ('c', 'celsius'): lambda x: x, # base
    ('k', 'kelvin'): lambda x: x + 273.15,
    ('f', 'fahrenheit'): lambda x: x * (9/5) + 32
}

time_zones = {
    ('NUT', 'WST', 'TOT', 'SST', 'TKT'): -11,
    ('HST', 'LINT', 'TAHT', 'CKT'): -10,
    'HDT': -9,
    ('AKDT', 'PST'): -8,
    ('MST', 'PDT'): -7,
    ('GALT', 'MDT', 'EAST'): -6,
    ('PET', 'ECT', 'COT', 'EST', 'CDT'): -5,
    ('CLT', 'BOT', 'GYT', 'VET', 'EDT'): -4,
    ('FKST', 'CLST', 'ART', 'PYT', 'BRT', 'GFT', 'SRT', 'ADT'): -3,
    'NDT': -2.5,
    ('WGST', 'CVT'): -1,
    'UTC': 0, # base
    ('GMT', 'AZOST'): 0,
    ('WEST', 'CET', 'IST', 'BST', 'WAT'): 1,
    ('SAST', 'CAT', 'CEST', 'EET'): 2,
    ('EAT', 'AST', 'EEST', 'IDT', 'MSK'): 3,
    'IRST': 3.5,
    ('RET', 'MUT', 'SCT', 'GST', 'AMT', 'AZT', 'GET', 'SAMT'): 4,
    'AFT': 4.5,
    ('TFT', 'MVT', 'PKT', 'TJT', 'UZT', 'YEKT', 'ORAT', 'TMT'): 5,
    ('IOT', 'BTT', 'KGT', 'OMST'): 6,
    'MMT': 6.5,
    ('ICT', 'HOWT', 'KRAT', 'NOVT', 'WIB'): 7,
    ('AWST', 'WITA', 'BNT', 'PHST', 'CST', 'HKT', 'ULAT', 'IRKT'): 8,
    ('WIT', 'JST', 'KST', 'YAKT', ): 9,
    'ACST': 9.5,
    ('AEST', 'PGT', 'ChST', 'VLAT'): 10,
    ('VUT', 'SBT', 'PONT', 'SRET'): 11,
    ('AoE', 'TVT', 'FJT', 'NZST', 'GILT', 'WAKT'): 12,
}

# ___________________________ Read CLI data ___________________________
###
# get data from CLI (case insensetive)
# example: > convert.py 12 Cm M -> [12, 'cm', 'm']
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

# ___________________________ Helper functions
# get factors from dictionaries
def get_factor(unit_dict, src, target):
    src_factor = target_factor = None
    for key, factor in unit_dict.items():
        # if key is a string or tuple element
        if (isinstance(key, tuple) and src in key) or key == src:
            src_factor = factor
        if (isinstance(key, tuple) and target in key) or key == target:
            target_factor = factor
    # stop converter if unknown key found
    if src_factor is None:
        print(f'Unknown source factor {src}')
        sys.exit(1)
    if target_factor is None:
        print(f'Unknown target factor {target}')
        sys.exit(1)
    return src_factor, target_factor

# ___________________________ Simple conversionts ___________________________
# --------------- weight, length, speed, time
def simple_convert(val, src, target, unit_dict): 
###
# 1) convert units to base (multiply value by dictionary value)
# 2) divide result from desired units dictionary value
# example: 12 cm km -> 12 * 0.01 (cm:0.01) -> 0.12 / 1000 (km:1000) -> 0.00012 km
###
    src_factor, target_factor = get_factor(unit_dict, src, target)
    # calculation
    if src_factor is not None:
        val = float(val)
        result = val * src_factor / target_factor
        print(f'{val}{src} = {round(result, 4)}{target}')

# ___________________________ Temperature conversion ___________________________
def temp_convert(val, src, target, unit_dict):
###
# 1) convert temperature to Celsius
# 2) convert Celsius to desired units
# example: 12 C K -> 12 (celsius is base, - if other) -> 12 + 273.15 -> 285.15
###
    # get conversion lambda functions
    src_factor, _ = get_factor(to_celsius, src, target)
    _, target_factor = get_factor(from_celsius, src, target)
    # calculate
    val = float(val)
    celsius = src_factor(val) 
    result = target_factor(celsius)
    # temperature units written in capital letters
    src = src.capitalize()
    target = target.capitalize()
    print(f'{val}{src} = {round(result, 2)}{target}')

# ___________________________ Time zone conversion ___________________________
def time_zone_convert(val, src, target):
    match = r'^([A-Z]{3,5})(?:([+-])(\d{1,2})(?::(\d{2}))?)?$'
    src_offset = target_offset = None
    
    # check if value correct format
    val_match = r'\d{1,2}:\d{1,2}$'
    if re.match(val_match, value) is None:
        print(f'For timezone conversion input value in 00:00 format')
        sys.exit(1)
    
    def parse_timezone(data):
        # get values from timezone input manually
        sign = data.group(2) # -/+
        hours = int(data.group(3)) # numbers before ':'
        minutes = int(data.group(4) or 0) # numbers after ':' if exist
        offset = hours * 60 + minutes
        if sign == '-':
            offset = -offset
        return offset
    
    src = src.upper()
    target = target.upper()
    list_src = re.match(match, src)
    list_target = re.match(match, target)
    # check if offset symbol exist, if doesn't check dictionary for offset
    if list_src.group(2) is None: 
        source_factor, _ = get_factor(time_zones, src, 'UTC') # parse default value to not get error (for not used result)
        src_offset = int(source_factor * 60)
    # if does divide string manually
    else:
        src_offset = parse_timezone(list_src)
    if list_target.group(2) is None:
        _, target_factor = get_factor(time_zones, 'UTC', target) 
        target_offset = int(target_factor * 60)
    else:
        target_offset = parse_timezone(list_target)
    # check if both values are found and convert
    if src_offset is not None and target_offset is not None:
        val_h, val_min = map(int, val.split(':'))
        offset = val_h * 60 + val_min
        total_offset_min = offset - src_offset + target_offset
        total_offset_min %= 24 * 60 # wrap in 24 hours
        result_h = total_offset_min // 60
        result_min = total_offset_min % 60
        print(f'{val_h:02}:{val_min:02} {src} = {result_h:02}:{result_min:02} {target}')
        return True
    return False

# ___________________________ Regex conversion handling ___________________________
###
# used for 1 to 1 conversions, like binary <-> number, or time-zones
# keep dictionary with regex patterns for keys and what function they need for conversion instead normal values
# call function directly based on key
###
# matches
timezone_regex = r'^[a-z]{3,5}(?:[+-]\d{1,2}(?::\d{2})?)?$' # find letters, letters + hours, letters + hours + minutes

# regex pattern dictionary
regex_dict = {
    re.compile(timezone_regex): time_zone_convert
}

def choose_regex_convert(val, src, target):
    for pattern, func in regex_dict.items():
        if re.match(pattern, src) and re.match(pattern, target):
            func(val, src, target)
            return True
    return False

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

done = False # check if conversion done
# check for same directory keys
all_key = []
source_dict = None
target_dict = None

for kind, unit_dict, conversion_type in conversions:
    if kind == 'simple':
        # go through all keys and check if both src and target in dictionaries
        for key in unit_dict:
            # if keys is tuple, flatten and add to list
            if isinstance(key, tuple):
                all_key.extend(key)
            # if key is a string, add to list
            else:
                all_key.append(key)
        # save source and target dicts to see if keys in same dict
        if source in all_key:
            source_dict = unit_dict
        if target in all_key:
            target_dict = unit_dict
        # run conversion only if both keys are in same directory
        if source_dict == target_dict and source_dict is not None:
            conversion_type(value, source, target, source_dict)
            done = True
            break
    elif kind == 'regex':
        if conversion_type(value, source, target):
            done = True
            break
    if done: 
        break
else:
    print(f'Cannot convert {source} to {target}')