"""
Display the per-commit size of the current git branch.
"""

import subprocess
import re
import sys
import os
import argparse
import shutil
import json
from pybars import Compiler
from datetime import datetime

repo=''
plan=''
#git log --pretty=format:"%h%x09%ad %s" --date=short --shortstat --reverse

def main():
  compiler = Compiler()
  file = open('./template/index.html.hb', 'r')
  template = compiler.compile(file.read())

  git = subprocess.Popen(['git', 'log', '--pretty=format:"%h%x09%ad %s"', '--shortstat', '--reverse'], stdout=subprocess.PIPE, cwd=repo)
  out_raw, err = git.communicate()
  out = out_raw.decode()
  total_lines = 0
  
  repo_info = []
  lines = out.split('\n')

  i = 0
  while i < len(lines):
    line = lines[i]
    if not line or line == '': 
      i += 1
      continue

    # Grab the last commit if multiple exist
    while lines[i+1][0] != ' ':
      i += 1
      line = lines[i]

    # This is a description line
    data = re.findall(r'(\w+)\s+([\w\s:]+)\s+[\+\-]\d+\s+(.*)', line)
    hash = data[0][0]
    date = data[0][1]
    desc = data[0][2][0:-1]

    # This is a stat line
    i += 1
    line = lines[i]
    data = re.findall(r'\s(\d+)\D+(\d+)(\D*)([\d?]*)', line)

    if len(data[0]) == 4 and data[0][3] != '':
      # This is a line that has insertions and deletions
      files = int(data[0][0])
      insertions = int(data[0][1])
      deletions = int(data[0][3])

      total_lines += (insertions - deletions)
    else:
      files = int(data[0][0])
      changed = int(data[0][1])
      type = data[0][2]
      if 'deletions' in type:
        total_lines -= changed
      else:
        total_lines += changed

    repo_info.append({'x': date, 'y': total_lines, 'desc': desc, 'hash': hash})
    i += 1
  
  if not os.path.exists('./output'):
    os.mkdir('./output')  
  
  plan_info = []
  with open(plan, 'r') as file:
    plan_info = json.load(file)
  
  for i in range(len(plan_info)):
    plan_info[i]['x'] = datetime.strptime(plan_info[i]['x'], '%b %Y').strftime('%a %b %d %H:%M:%S %Y')

  output = template({'commits': repo_info, 'plan': plan_info})
  with open('./output/index.html', 'w') as file:
    file.write(output)
  
  shutil.copyfile('./template/canvasjs.min.js', './output/canvasjs.min.js')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='gitgraph', description='Visual git statistics', epilog='Because SLOC matters!')
  parser.add_argument('-r', '--repo')
  parser.add_argument('-p', '--plan')
  args = parser.parse_args()
  repo = args.repo
  plan = args.plan
  sys.exit(main())