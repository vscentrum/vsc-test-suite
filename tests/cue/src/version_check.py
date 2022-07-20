
import sys
import os
import subprocess
from pkg_resources import parse_version as version
import re
import json


tool = json.loads(sys.argv[1])

try:
    ver_opt = tool['veropt']
except:
    ver_opt = '--version'

try:
    options = tool['options']
except:
    options = ""

cmd = f"{tool['exe']} {ver_opt} {options}"
out = subprocess.run([cmd],shell=True, stdout=subprocess.PIPE)
out = out.stdout.decode('utf-8')

try:
    regular = tool['re']
except:
    regular = r'(?:(\d+\.(?:\d+\.)*\d+))'
match = re.findall(regular, out)

print(version(tool['minver']) <= version(match[0]))  # True
