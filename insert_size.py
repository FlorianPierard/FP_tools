#!/usr/bin/env python3

# =============================================================================
# Author: Florian Pierard
# Email: florian.pierard@gmail.com
# Last update: 10 September 2020
# =============================================================================
Description = '''This script analyze the insert size of your paired end reads.
It takes as arguments the bam file and write the output in the same
directory.'''
# =============================================================================
# Import
# =============================================================================
import os
import matplotlib.pyplot as plt
import pysam
import pandas as pd
import numpy as np
import sys
import collections
#==============================================================================
# Arguments
#==============================================================================
bam_file = sys.argv[1]
#==============================================================================
# Functions
#==============================================================================
def insert_size(bam_file):
    output_dir = os.path.dirname(bam_file)
    insert_plot = os.path.join(output_dir, "Insert_size.png")
    insert_txt = os.path.join(output_dir, "Insert_sizes.csv")
    #------------------------------------------
    # Insert size with the bam file
    #------------------------------------------
    SamFile = pysam.AlignmentFile(bam_file, "rb")
    insert_sizes = []
    for read in SamFile:
        if read.is_read2: # avoid couting reads twice
            continue
        if not read.is_paired or read.is_unmapped: # only good reads
            continue
        insert_sizes.append(abs(read.tlen))
    insert_sizes.sort()
    insert_sizes = np.array(insert_sizes)
    # Check reads between 250 and 450 of length.
    good_inserts = np.logical_and(insert_sizes > 250, insert_sizes < 450)
    percentage_good_inserts = good_inserts.sum() * 100 / len(insert_sizes)
    IQRs = np.percentile(insert_sizes, (25, 50, 75, 99))
    print("25th percentile:", IQRs[0])
    print("50th percentile (median):", IQRs[1])
    print("75th percentile:", IQRs[2])
    print("Percentage of reads between 250 and 450:", round(
        percentage_good_inserts, 2))
    insert_size_dict = collections.Counter(insert_sizes)
    pd_dict = {"Insert_size": list(insert_size_dict.keys()),
               "Occurences": list(insert_size_dict.values())
               }
    pd.DataFrame.from_dict(pd_dict).to_csv(insert_txt, index = False)
    # Generating the plot
    plt.figure(figsize=(30, 10), dpi=80, facecolor='w', 
               edgecolor='k')
    plt.bar(insert_size_dict.keys(), insert_size_dict.values(), color = "r",
            width = 0.6)
    plt.title("Insert size distribution", size = 40)
    plt.xticks(np.arange(0, IQRs[3], 50),size = 10)
    plt.xlim((0, IQRs[3]))
    plt.yticks(size=20)
    # Ad a line to show an eventual threshold
    plt.ylabel("Occurences",   size = 30)
    plt.xlabel("Insert size, median: %s" % int(IQRs[1]),size = 30)
    plt.tight_layout()
    plt.savefig(insert_plot)
    plt.close()

#==============================================================================
#			       ! ! ! ! !  START OF THE ANALYSIS  ! ! ! ! !
#==============================================================================
if __name__ == "__main__":
    insert_size(bam_file)
