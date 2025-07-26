# ___________________________ Dependencies ___________________________
import sys

# ___________________________ Base dictionaries ___________________________
###
# dictionaries keep all values and how to convert them to 'base'
# example: cm to m, km to m, lbs to g, kg to g
# then base result converted to desired units (no need for if-else/choice hell)
###
length_units = {
    
}

weight_units = {
    
}

speed_units = {
    
}

time_units = {
    
}

to_celsius = {
    
}

from_celsius = {
    
}

timezones = {
    
}

# ___________________________ Read CLI data ___________________________
###
# get data from CLI
# example: > convert.py 12 cm m -> [12, 'cm', 'm']
###
argv = sys.argv[1:]
if len(argv) != 3:
    print('Wrong input, example - python convert.py 12 cm m')
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
# --------------- weight
def weight_convert():
    return

# --------------- length
def length_convert():
    return

# --------------- time
def time_convert():
    return

# --------------- speed
def speed_convert():
    return

# ___________________________ Temperature conversion ___________________________
###
# similar to simple conversions
# 1) convert temperature to Celsius
# 2) convert Celsius to desired units
# example: 12 C K -> 12 (celsius is base, - if other) -> 12 + 273.15 -> 285.15
###
def temp_convert():
    return

# ___________________________ Time zone conversion ___________________________
###
# similar to simple conversions
# 1) convert everything to UTC (example: EDT+6 -> UTC+6)
# 2) convert to UTC+0 (by subtracting number after letters)
# 3) convert to desired displacement (add number after letters)
# example: 4:30 EDT-2 GMT+4.30
# 4:30 EDT-2 -> 4:30 UTC-2 -> 6:30 UTC+0 -> 11:00 UTC+4.30
###
def time_zone_convert():
    return