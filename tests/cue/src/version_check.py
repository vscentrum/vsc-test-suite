
import sys
import subprocess
from pkg_resources import parse_version as version
import re

args = list(sys.argv)

cmd = f"rpm -q {args[1]}"
out = subprocess.run([cmd],shell=True, stdout=subprocess.PIPE)
out = out.stdout.decode('utf-8')

if re.search(r'not installed', out):
    cmd = f"{args[1]} --version"
    out = subprocess.run([cmd],shell=True, stdout=subprocess.PIPE)
    out = out.stdout.decode('utf-8')

out = [line for line in out.split('\n') if line.strip() != '']
out = out[0]
match = re.findall(r'(?:(\d+\.(?:\d+\.)*\d+))', out)

print(version(args[2]) <= version(match[0]))  # True
