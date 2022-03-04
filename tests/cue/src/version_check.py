
import sys
import os
import subprocess
from pkg_resources import parse_version as version
import re
import json


tool=json.loads(sys.argv[1])

cmd = f"rpm -q {tool['exe']}"
out = subprocess.run([cmd],shell=True, stdout=subprocess.PIPE)
out = out.stdout.decode('utf-8')

try:
    flag = tool['skiprpm']
except:
    flag = False

if re.search(r'not installed', out) or flag:
    cmd = f"{tool['exe']} {tool['options']}"
    out = subprocess.run([cmd],shell=True, stdout=subprocess.PIPE)
    out = out.stdout.decode('utf-8')

out = [line for line in out.split('\n') if line.strip() != '']
out = out[0]

try:
    regular = tool['re']
except:
    regular = r'(?:(\d+\.(?:\d+\.)*\d+))'
match = re.findall(regular, out)

print(version(tool['minver']) <= version(match[0]))  # True
