# Oneline-CLI-converter
### Idea
Convert units in CLI using 1 line, idea is to make it as fast and simple as possible to rationalize using it instead of finding converter in the web. That means - no installed libraries, just pure python and conversion should happen from single input using least possible values.
### Usage
In CLI (terminal) input the .py path and info that you have and get answer:
> python path/to/convert.py value unit_have unit_want
1) have python on main system
2) clone repo or download zip and extract .py file
3) use python (in Windows 'py', in Linux 'python3')
4) input path to convert.py file (or just convert.py after py/python3 if in same directory)
5) input value that you have
6) what units that value is
7) the units you wish to convert to
### Examples (assuming .py in the current directory)
- length 
  - py convert.py 12 cm meter
  - 12cm = 0.12meter
- timezone
  - python3 convert.py 12:00 ECT UTC+3
  - 12:00 ECT = 20:00 UTC+3
### Notes
- Conversions support unit name and symbol (m to kilometer, s to min, feet to kilometer)
- Time zone conversions support abreviation, offset or country name (UTC+3 to EST, EST to WST, CLT-4 to London)
- Some timezone abreviations have multiple meanings (for example CST is China +8 hours and Mexico -6 hours) so conversion will show every posibility if using just abreviation and not city/manual offset
- Time zone conversions doesn't show date (if time goes after 23:59 or before 00:01, no notice of different day will be shown)
- Possible conversions: (names are only accepted as singular, except 'feet')
  - length (pm, nm, um, mm, cm, m, km, inch, ft, yard, mile) (works with names like: meter, feet...)
  - weight (pg, ng, ug, mg, g, kg, ton, oz, lbs) (works with name: gram, ounce)
  - time (ps, ns, us, ms, s, min, h, day, week, month, year) (works with names: second, minute)
  - speed (cm/s, m/s, m/min, km/s, km/min, km/h, ips, fps, mph, knot)
  - time zones (no offset - ECT, offset - UTC+3, country - Germany)
  - temperature (K, C, F) (works with name: celsius, kelvin)
