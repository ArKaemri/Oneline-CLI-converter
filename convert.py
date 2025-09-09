# ___________________________ Dependencies ___________________________
import sys
import re
import pytz
from datetime import datetime
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
    ('GALT', 'MDT', 'EAST', 'CST'): -6,
    ('PET', 'ECT', 'COT', 'EST', 'CDT'): -5,
    ('CLT', 'BOT', 'GYT', 'VET', 'EDT', 'AST', 'AMT'): -4,
    ('FKST', 'CLST', 'ART', 'PYT', 'BRT', 'GFT', 'SRT', 'ADT'): -3,
    'NDT': -2.5,
    'GST': -2,
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

all_zones = pytz.all_timezones
# ___________________________ Read CLI data ___________________________
###
# get data from CLI (case insensetive)
# example: > convert.py 12 Cm M -> [12, 'cm', 'm']
###
argv = sys.argv[1:]
if len(argv) != 3:
    print('Wrong input, example - python convert.py 12 cm m')
    sys.exit(1)
argv = [x.lower() for x in argv]
value = argv[0]
source = argv[1]
target = argv[2]

# ___________________________ Helper functions
# get factors from dictionaries
def get_factor(unit_dict, src, target):
###
# check if key is in dictionary and it is standalone or part of a tuple
# if it is, return value of that key
###
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

def get_timezone_offset(type):
###
# check if timezone matches single word (city) or timezone regex
# if so, check which type:
#                           standalone abreviation (CST)
#                           manual offset (PST-8)
#                           city name (London)
# after finding the type, extract the offset in minutes compared to UTC-0
###
    city_regex = r'^[a-z]+$'
    offset_regex = r'^([a-z]{3,5})(?:([+-])(\d{1,2})(?::(\d{2}))?)?$'
    output  = re.match(offset_regex, type)
    # get city offset by city
    if re.match(city_regex, type):
        # convert city into IANA format
        city = type.capitalize()
        iana = [x for x in all_zones if city in x.split('/')]
        # if list not empty (found the IANA format)
        if iana:
            # create timezone object
            zone = pytz.timezone(iana[0])
            timezone = datetime.now(zone)
            # get the offset from UTC-0 and split into h/min
            time = str(timezone.utcoffset()).split(':')
            # convert to minutes
            offset = int(time[0]) * 60 + int(time[1])
            return city, offset 
    # if city or abreviation regex didn't found anything, break the conversion
    if output is None:
        print(f'unknown timezone {type}')
        sys.exit(1)
    # go through dict, save offset list
    if output.group(2) is None:
        offsets = {}
        type = type.upper()
        for zone, offset in time_zones.items():
            # if key is tuple
            if isinstance(zone, tuple):
                for z in zone:
                    if type == z:
                        offsets.setdefault(z, []).append(offset)
            else:
                if type == zone:
                    offsets.setdefault(z, []).append(offset)
        # convert each offset to minutes
        offsets = {key: [v * 60 for v in value] for key, value in offsets.items()}
        key, value = next(iter(offsets.items()))
        return key, value
    # manually extract offset
    elif output.group(2) is not None:
        zone = output.group(1).upper()
        sign = output.group(2)
        h = int(output.group(3))
        min = int(output.group(4) or 0)
        offset = h * 60 + min
        if sign == '-':
            offset = -offset
        return zone, offset
    
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
        print(f'{val} {src} = {round(result, 4)} {target}')

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
    print(f'{val} {src} = {round(result, 2)} {target}')

# ___________________________ Time zone conversion ___________________________
def time_zone_convert(val, src, target):
###
# get offsets of timezones compared to UTC-0
# subtract source offset to value, then add target
###
    src_offset = target_offset = None
    # check if value format is correct (time input)
    val_match = r'^\d{1,2}:\d{1,2}$'
    if re.match(val_match, val) is None:
        print(f'For timezone conversion input value in 00:00 format')
        sys.exit(1)
    # get offsets
    src_zone, src_offset = get_timezone_offset(src)
    target_zone, target_offset = get_timezone_offset(target)
    
    # convert time from source zone to target zone
    def calculate_time(offset_src, offset_target):    
        val_h, val_min = map(int, val.split(':'))
        offset = val_h * 60 + val_min
        total_offset_min = offset - offset_src + offset_target
        total_offset_min %= 24 * 60
        result_h = total_offset_min // 60
        result_min = total_offset_min % 60
        print(f'{val_h:02}:{val_min:02} {src_zone} = {result_h:02}:{result_min:02} {target_zone}\n')

    # if src or target has list of offsets, iterate the list
    if isinstance(target_offset, list) and isinstance(src_offset, list):
        for offset_s in src_offset:
            for offset_t in target_offset:
                calculate_time(offset_s, offset_t)
    elif isinstance(src_offset, list):
        for offset in src_offset:
            calculate_time(offset, target_offset)
    elif isinstance(target_offset, list):
        for offset in target_offset:
            calculate_time(src_offset, offset)
    else:
        calculate_time(src_offset, target_offset)


# ___________________________ Regex conversion handling ___________________________
###
# used for non number<->number conversions, like binary <-> number, or time-zones
# keep dictionary with regex patterns for keys and what function they need for conversion instead normal values
# call function directly based on key
###
# matches
timezone_offset_regex = r'^[a-z]{3,5}(?:[+-]\d{1,2}(?::\d{2})?)?$' # find letters, letters + hours, letters + hours + minutes
timezone_city_regex = r'^[a-z]+$'

# regex pattern dictionary
regex_dict = {
    re.compile(timezone_offset_regex): time_zone_convert,
    re.compile(timezone_city_regex): time_zone_convert
}

def choose_regex_convert(val, src, target):
    # loop through unique functions
    for func in set(regex_dict.values()):
        # check if any regex of same function matches input
        src_match = any(re.match(pattern, src) for pattern, f in regex_dict.items() if f is func)
        target_match = any(re.match(pattern, target) for pattern, f in regex_dict.items() if f is func)
        if src_match and target_match:
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

###
# loop through conversion dictionary to find if conversion simple or regex based
# if conversion simple: 
#   - get all keys from dictionary (flatten the dict)
#   - if source and target units are in found keys, save the dictionary
#   - if target and source values were in same dictionary, use conversion
#   - if only 1 value in keys, 1 value will be None and conversion won't happen, on new
#     loop, there will be new dictionary and both values set back to None, so both will 
#     never be not None on different source and target values
# else call regex function
# if neither happened, keys are either from different dictionaries or wrong units provided, print output
###
done = False # check if conversion done
for kind, unit_dict, conversion_type in conversions:
    # check for same directory keys
    all_key = []
    source_dict = None
    target_dict = None
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
        if source_dict is not None and target_dict is not None:
            conversion_type(value, source, target, source_dict)
            done = True
            break
    elif kind == 'regex':
        conversion_type(value, source, target)
        done = True
        break
    if done: 
        break
else:
    print(f'Cannot convert {source} to {target}')