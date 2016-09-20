#!/usr/bin/env python

import argparse
import mmap
import os
import re
import sys
import glob
import subprocess
import inspect

class colors:
    RED='\033[91m'
    GREEN='\033[92m'
    END='\033[0m'

req_folders = ["active", "err-log", "pidstat", "netmon", "diskusage", "rhizome-general", "servald-general", "serval-logs", "ntp-log"]

inc_folders = []

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
def check_file(dirname):
    base_dirname = '/'.join(dirname.split('/')[:-1])
    for filename in os.listdir(dirname):
        if file_len(dirname + '/' + filename) <= 1:
            if base_dirname not in inc_folders:
                print "There are empty logs in " + colors.RED +  dirname + colors.END + '. ' + colors.RED + filename + colors.END + ' is strange. This should be investigated.'
                inc_folders.append(base_dirname)

def check_rhizome_general(dirname):
    if "-file" in dirname and 'rhizome-general' in dirname:
        check_file(dirname)

def check_servald_general(dirname):
    if 'servald-general' in dirname:
        check_file(dirname)

def check_diskusage(dirname):
    if 'diskusage' in dirname:
        check_file(dirname)

def check_netmon(dirname):
    if 'netmon' in dirname:
        check_file(dirname)

def check_pidstat(dirname):
    if 'pidstat' in dirname:
        check_file(dirname)

def check_active(dirname):
    if 'active' in dirname:
        check_file(dirname)

def check_error(dirname):
    base_dirname = '/'.join(dirname.split('/')[:-1])
    if 'err-log' in dirname:
        if len(subprocess.check_output('./show-errors-in-logs ' + dirname, shell=True)):
            print 'Errors occured in ' + colors.RED + base_dirname + colors.END + '. This should be investigated.'
            inc_folders.append(base_dirname)

def run_is_complete(run_folder):
    result=True
    nodes=glob.glob(run_folder + "/qemu*.sid")
    contents=glob.glob(run_folder + "/*")
    dirs=filter(os.path.isdir, contents)

    if len(os.listdir(run_folder)) <= 4:
        print colors.RED + run_folder + colors.END
        print "Contains only " + str(len(os.listdir(run_folder))) + " elements: " + ", ".join(os.listdir(run_folder))
        result=False
    for dirname in dirs:
        if not os.path.basename(os.path.normpath(dirname)) in req_folders and len(nodes) != len(os.listdir(dirname)):
            if result:
                print colors.RED + run_folder + colors.END
            print "There are elements missing in " + dirname + ": got " + str(len(os.listdir(dirname))) + ", expected - " + str(len(nodes))
            result=False
        check_rhizome_general(dirname)
        check_servald_general(dirname)
        check_diskusage(dirname)
        check_netmon(dirname)
        check_pidstat(dirname)
        check_active(dirname)
        check_error(dirname)
    return result

def search_folder(folder, depth, complete):
    dirs=glob.glob(folder + "/*" * (depth))
    incomplete_count=0
    complete_runs=[]
    for dir in dirs:
        if not run_is_complete(dir):
            incomplete_count += 1
        elif complete:
            complete_runs.append(dir)
    incomplete_count += len(inc_folders)
    print (colors.RED if incomplete_count > 0 else colors.GREEN) + str(incomplete_count) + "/" + str(len(dirs)) + " runs incomplete" + colors.END + "\n"
    if complete:
        print "\n".join(complete_runs)
        print colors.GREEN + str(len(complete_runs)) + "/" + str(len(dirs)) + " runs complete" + colors.END + "\n"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="the log folder to analyze")
    parser.add_argument("depth", type=int, help="the relative depth of the run folders")
    parser.add_argument("--complete", help="also show all completed runs", action="store_true")
    return parser.parse_args()

if __name__=='__main__':
    args=parse_args()
    search_folder(**vars(args))
