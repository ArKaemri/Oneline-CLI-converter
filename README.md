# Oneline-CLI-converter
### Idea
Convert units in CLI using 1 line, idea is to make it as fast and simple as possible to rationalize using it instead of finding converter in the web. That means - no installed libraries, just pure python and conversion should happen from single input using least possible values.
### Usage
In CLI (terminal) input the .py path and info that you have and immediately get answer:
> python path/to/convert.py value unit_have unit_want
1) have python on main system
2) clone repo or download zip and extract .py file
3) use python (in Windows 'py', in Linux 'python3')
4) input path to .py file (or just .py file if in same directory)
5) input value that you have
6) what units that value is
7) the units you wish to convert to
### Examples (assuming .py in the current directory)
- length in Windows
  - py convert.py 12 cm m
  - 12cm = 0.12m
- timezone in Linux
  - python3 convert.py 12:00 UTC-3 GMT+3:45
  - 12:00 UTC-3 = 18:45 DMT+3:45
### Notes
- Conversions is done by unit symbols, not names (m for meter, C for Celsius, g for gram)
- Time zone conversions require offset (EEST+3 instead of EEST, offset is based from UTC)
- Time zone conversions doesn't show date (if time goes after 23:59 or before 00:01, no notice of different day will be shown)
- After wrong conversion input all possible conversions will be displayed on terminal
- Possible conversions:
  - length (pm, nm, um, mm, cm, m, km, inch, ft, yard, mile)
  - weight (pg, ng, ug, mg, g, kg, ton, oz, lbs)
  - time (ps, ns, us, ms, s, min, h, day, week, month, year)
  - speed (cm/s, m/s, m/min, km/s, km/min, km/h, ips, fps, mph, knot)
  - time zones (example: GMT+3 to UTC-7:30 -> 2 to 4 symbols, +/-, single value (hour) or hour:minutes)
  - temperature (K, C, F)
