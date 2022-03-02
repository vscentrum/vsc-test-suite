
import sys
import subprocess
from pkg_resources import parse_version as version
import re

args = list(sys.argv)

cmd = f"rpm -q {args[1]}"
out = subprocess.run([cmd],shell=True, stdout=subprocess.PIPE)
out = out.stdout.decode('utf-8')

if re.search(r'not installed', out):
    cmd = f"{args[1]} --version | sed 1q"
    out = subprocess.run([cmd],shell=True, stdout=subprocess.PIPE)
    out = out.stdout.decode('utf-8')

with open('data', 'w') as file:
    file.write(out)
    
out = subprocess.run(['sed', r's/^.*[^0-9]\([0-9]*\.[0-9]*\.[0-9]*\).*$/\1/', 'data'], stdout=subprocess.PIPE)
out = out.stdout.decode('utf-8')
print(version(args[2]) <= version(out))  # True

