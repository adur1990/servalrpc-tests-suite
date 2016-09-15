#!/usr/bin/env python

from __future__ import print_function
import argparse
import mmap
import os
import re
import sys

def parameterlist_is_valid():
  return ((len(sys.argv) == 4 or len(sys.argv) == 3)
    and os.path.isdir(sys.argv[1]) and is_valid_regex(sys.argv[2]))

def is_valid_regex(string):  
  try:
    re.compile(string)
    is_valid = True
  except re.error:
    is_valid = False
  return is_valid

def is_non_empty_file(fpath):  
  return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def search_folder(folder, query, extension):
  for subdir, dirs, files in os.walk(folder):
    for fname in files:
      filepath=os.path.join(subdir, fname)
      if is_non_empty_file(filepath) and fname.endswith(extension):
        f = open(filepath)
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if re.search(br'(?i)' + query, s):
          print('\n')
          print('#' * (len(filepath)+4))
          print('# ' + filepath + ' #')
          print('#' * (len(filepath)+4))
          for line in iter(s.readline, ""):
            if re.search(br'(?i)' + query, line):
              print(line[:-1])

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("folder", default=argparse.SUPPRESS)
  parser.add_argument("-f", "--folder", dest="folder")
  parser.add_argument("query", default=argparse.SUPPRESS)
  parser.add_argument("-q", "--query", dest="query")
  parser.add_argument("extension", nargs='?', default=argparse.SUPPRESS)
  parser.add_argument("-e", "--extension", dest="extension", default='')  
  return parser.parse_args()
  
if __name__=='__main__':
  args=parse_args()
  search_folder(**vars(args))
