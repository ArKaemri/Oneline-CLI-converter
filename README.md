# Oneline-CLI-converter
### Idea
Convert units in CLI using 1 line (not choices), idea is to make it as fast and simple as possible to rationalize using it instead of find converter in the web. That means - no installed libraries, just pure python so there is no need to clutter main system or create environment and conversion should happen from single input from least possible values.
### Working principle
In CLI (terminal) input the .py path and info that you have and immediately get answer:
> python convert.py value unit_have unit_want
1) clone repo or download zip and extract .py file
2) use python (in Windows 'python', in Linux 'python3')
3) input path to .py file (or just .py file if in same directory)
4) input the numeric value that you have
5) what units that value is
6) the units you wish to convert to
### Examples (assuming .py in the current directory)
- python convert.py 12 cm m
- 12cm = 0.12m

- python convert.py 12:00 UTC-3 GMT+3:45
- 12:00 UTC-3 = 18:45 DMT+3:45
### Notes
Currently script supports: 
- length (pm, nm, um, mm, cm, m, km, inch, ft, yard, mile)
- weight (pg, ng, ug, mg, g, kg, ton, oz, lbs)
- time (ps, ns, us, ms, s, min, h, day, week, month, year)
- speed (cm/s, m/s, m/min, km/s, km/min, km/h, ips, fps, mph, knot)
- time zones (exmaple: GMT+3 to UTC-7 -> 2 to 4 symbols, +/-, single value (hour) or hour:minutes)
- temperature (K, C, F)
