#!/usr/bin/env python

from subprocess import check_output
import os
from pprint import pprint
import re
from shlex import split
from collections import OrderedDict

os.system('./miniworld-execute-par "/usr/bin/date +%s%3N" 2> qemu_dates.txt')

with open("qemu_dates.txt", "r") as f:
	times = f.read()
	#print "times from qemu nodes: \n%s" % times
        times = re.findall("(\d+)\s+[:]\s+(\d+)", times)
        #print times
        times = sorted(map(lambda (x,y) : (int(x), int(y)), times))
        #print times

times_by_lines = OrderedDict(times).values()
#print times_by_lines

def get_pairwise_time_diff():
	print "time diff:"
	diff_list = map(lambda (cnt, (x, y)): ("%s,%s" % (cnt, cnt+1), y-x), enumerate(zip(times_by_lines, times_by_lines[1:]), 1))
        pprint(diff_list)

get_pairwise_time_diff()
