#!/usr/bin/env python

# diff_lumisections.py
#
# This script takes two lumi cache directories from the public plots script and compares them to see if there
# are any lumisections that are in one but not the other. It can be used, for example, to see if there are
# any discrepancies between the online and normtag lumi caches for a given year.

import argparse, csv, glob

parser = argparse.ArgumentParser()
parser.add_argument("dir1", help="First input directory")
parser.add_argument("dir2", help="Second input directory")
args = parser.parse_args()

# This stores the lumisections present for the files in each directory.
lumisections_present = [{}, {}]

for i, dir_name in enumerate([args.dir1, args.dir2]):
    for infile in glob.iglob(dir_name+"/lumicalc_cache_????-??-??.csv"):
        with open(infile) as csv_input:
            reader = csv.reader(csv_input, delimiter=',')
            
            for row in reader:
                if row[0][0] == '#':
                    continue
                run = int(row[0].split(":")[0])
                ls = int(row[1].split(":")[0])
                if run not in lumisections_present[i]:
                    lumisections_present[i][run] = set()
                lumisections_present[i][run].add(ls)

            # loop over rows
        # open file
    # loop over files in directory
# loop over directories
 
# Make this a subroutine so we don't have to do this twice
def print_differences(a, b):
    tot = 0
    for r in sorted(a.keys()):
        # Find difference between a and b for this run
        if r not in b:
            d = sorted(a[r])
        else:
            d = sorted(a[r] - b[r])
        if len(d) > 0:
            # This is /probably/ a continuous range, but in the case that it's not,
            # go through to find the individual ranges
            ranges = ""
            startLS = d[0]
            endLS = d[0]
            for i in d[1:]:
                if (i != endLS+1):
                    # start of a new range
                    if (startLS == endLS):
                        ranges += str(startLS)+" "
                    else:
                        ranges += str(startLS)+"-"+str(endLS)+" "
                    startLS = i
                endLS = i
            # don't forget to get the very last one
            if (startLS == endLS):
                ranges += str(startLS)+" "
            else:
                ranges += str(startLS)+"-"+str(endLS)+" "
            print str(r)+":"+ranges
            tot += 1
    if tot == 0:
        print "none"

print "Lumisections in",args.dir1,"but not in",args.dir2+":"
print_differences(lumisections_present[0], lumisections_present[1])
print "Lumisections in",args.dir2,"but not in",args.dir1+":"
print_differences(lumisections_present[1], lumisections_present[0])
