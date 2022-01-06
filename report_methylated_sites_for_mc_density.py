#!/usr/bin/env python

## when need to know density of mC per some window
## start by making a file that has all the sites that you consider methylated -- this is somewhat subjective
## so here you can play with that 
## input file is raw bsmap output, with all contexts combined
## output is those lines of input that are methylated per context
## for instance: 
## to include all contexts over 10% threshold, use:
## 
##   ./report_methylated_sites_for_mc_density.py  single_c_gff  0.1 0.1 0.1 > outfile
## 
## while if you want those with >10% mCHH, >30% mCHG, and >60% mCG, use 
##
##  ./report_methylated_sites_for_mc_density.py  single_c_gff  0.1 0.3 0.6 
##
## to completely exclude a particular context, then use a value greater than 1 
## so for non-CG meth density only, use 0.1 0.1 1.1 for instance

import sys, time

if len(sys.argv) == 1: # no arguments, so print help message
        print("""\n"""
                """Usage: ./report_methylated_sites_for_mc_density.py  single_c_gff  mCHH_cutoff  mCHG_cutoff  mCG_cutoff\n"""
                """where cutoffs are values between 0 and 1\n"""
                """\n""")

input1=sys.argv[1]

mCHH_cutoff=float(sys.argv[2])
mCHG_cutoff=float(sys.argv[3])
mCG_cutoff=float(sys.argv[4])



with open(input1, 'r') as methfile:

    result=[]

    for i in methfile.readlines():
        i=i.strip().split()

        if i[2]=='CHH' and float(i[5])>mCHH_cutoff:
            result.append(i)

        if i[2]=='CHG' and float(i[5])>mCHG_cutoff:
            result.append(i)

        if i[2]=='CG' and float(i[5])>mCG_cutoff:
            result.append(i)

    for i in result:
        i="\t".join(map(str,i))
        print i
