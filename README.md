# Oneline-CLI-converter
### Idea
Convert common units in CLI using 1 line (not choices), idea is to make it as fast and simple as possible to rationalize using it instead of find converter in the web.
### Working principle
In CLI input the script path and info that you have and immediately get answer:
- python convert.py 12 cm m
- 12cm = 0.12m
1) use python (in Windows 'python', in Linux 'python3')
2) input the numeric value that you have
3) what units that value is
4) the units you wish to convert to
### Notes
Currently script supports: 
- length (mm, m, cm, km, feet, inches, miles)
- weight (g, kg, mg, lbs)
- time (ms, s, minutes, hours, days)
- speed (m/s, km/h, km/s, mile/minute)
- time zones (GMT+3 to UTC-7)
- temperature (Kelvin, Celsius, Fahrenheit)
In the future planning to add non numeric conversions, like:  binary to number, hexadecimal to binary, hexacode to rgb, rgb to grayscale ...