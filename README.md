# Oneline-CLI-converter
### Idea
Convert common units in CLI using 1 line (not choices), idea is to make it as fast and simple as possible to rationalize using it instead of find converter in the web.
### Working principle
In CLI input the script path and info that you have and immediately get answer:
> python convert.py 12 cm m
> 12cm = 0.12m
First 'activate' python (in Windows 'python', in Linux 'python3'), then input the numeric value that you have, then what units that value is and in the end the units you wish to convert to.
### Notes
Currently script supports: length, weight, time, speed, time zones (GMT+3 to UTC-7) and temperature. In the future planning to add non numeric conversions, like:  binary to number, hexadecimal to binary, hexacode to rgb, rgb to grayscale ...