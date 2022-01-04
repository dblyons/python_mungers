#!/usr/bin/env python


import numpy as num
import pybedtools
import sys

infile1=sys.argv[1]
infile2=sys.argv[2]

outfile1=sys.argv[3]
outfile2=sys.argv[4]
outfile3=sys.argv[5]
outfile4=sys.argv[6]
outfile5=sys.argv[7]

print '\n'
print 'usage: metanuc.py <infile1.bed> <infile2.bed> group1,-2,-3,-4,nongroup ...7 files required...\n'
print 'infile must be simple 3col bed\n'
print 'use the following commands to filter inps gathered output to make this 3col bed:\n'
print "#awk '$5 < 150 {print}' ...._Gathering.like_bed  \n#perl -wnl -e '/\sMainPeak\s/ and print;'\n#perl -wpl -e 's/^/Chr/g;' \n#awk '{print $1tab$2tab$3}'\n" 
print '\n'

a = pybedtools.BedTool(infile1)
b = pybedtools.BedTool(infile2)

aplusb = a.intersect(b, wo=True)

group1=0
group2=0
group3=0
group4=0
non_group=0
                                

for line in aplusb:
    line=list(line)
    
    
    nucOverlap1=float(line[6])/(float(line[2])-float(line[1]))
    nucOverlap2=float(line[6])/(float(line[5])-float(line[4]))
    meanOverlap=(nucOverlap1+nucOverlap2)/2
    estSize=float(line[6])/meanOverlap#use this to cutoff nucs that are too large.  try 120 bp for now.
    obsMeanSize= ((float(line[2])-float(line[1]))+(float(line[5])-float(line[4])))/2
    skewFromEstimate=round(estSize/obsMeanSize, 3)#can use this later if want to exclude overlapping nucs 
                                                    #with vastly different lengths - could suggest mnase screwy
                                                    #at those sites.  cutoff of <98% should do for group1.
    #get left end of metanuc (the leftmost and rightmost of the overlapping 2 nucs)
    coords=(int(line[1]), int(line[2]), int(line[4]), int(line[5]))
    left=min(coords)
    right=max(coords)
    
    line.append(round (nucOverlap1, 3))
    line.append(round (nucOverlap2, 3))
    line.append(round(meanOverlap, 3))
    line.append(round(estSize, 3))
    line.append(obsMeanSize)
    line.append(skewFromEstimate)
    line.append(left)
    line.append(right)
    
    #print line
    
    fh1=open(outfile1, 'a')
    fh2=open(outfile2, 'a')
    fh3=open(outfile3, 'a')
    fh4=open(outfile4, 'a')
    fh5=open(outfile5, 'a')
    
    
    
    
    
    if meanOverlap > 0.75 and skewFromEstimate > 0.98 and estSize < 120:
        g1interval=str(line[0])+'\t'+str(line[-2])+'\t'+str(line[-1])+'\n'
        fh1.writelines(g1interval)
        group1+=1
        
    elif meanOverlap > 0.5 and meanOverlap <= 0.75 and estSize < 120:
        g2interval=str(line[0])+'\t'+str(line[-2])+'\t'+str(line[-1])+'\n'
        fh2.writelines(g2interval)
        group2+=1
    elif meanOverlap > 0.25 and meanOverlap <= 0.5 and estSize < 120:
        g3interval=str(line[0])+'\t'+str(line[-2])+'\t'+str(line[-1])+'\n'
        fh3.writelines(g3interval)
        group3+=1
    elif meanOverlap < 0.25 and estSize < 120:
        g4interval=str(line[0])+'\t'+str(line[-2])+'\t'+str(line[-1])+'\n'
        fh4.writelines(g4interval)
        group4+=1
    else: 
        #rubbish heap
        fh5.writelines(str(line)+"\n")
        non_group+=1

print '\n'
print 'nucleosomes in each group for\n {}\n {}\n'.format(infile1, infile2)
print 'group 1: ',group1
print 'group 2: ',group2
print 'group 3: ',group3
print 'group 4: ',group4
print 'non_group: ',non_group
print '\n'
