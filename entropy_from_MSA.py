#!/usr/bin/env python3

# =============================================================================
# Author: Florian Pierard
# Email: florian.pierard@gmail.com
# Last update: 10 September 2020
# =============================================================================
Description = '''This script is made to make an entropy plot from a MSA. The 
entropy value is Shannon's entropy with log2.
The MSA is the only argument and the plot will be written in the same 
directory.'''

#==============================================================================
# Import
#==============================================================================
import sys
import numpy as np
from math import log2
from Bio import AlignIO
from collections import Counter
import matplotlib.pyplot as plt
#==============================================================================
# Arguments
#==============================================================================
MSA = sys.argv[1]
#==============================================================================
# Functions
#==============================================================================
def entropy(list_of_values):
    '''Return the entropy of a list of values. It doesn't count a value if 
    it is less than 5.'''
    entropy = 0
    np_elt = np.array(list_of_values)
    if not all(np_elt == 0):
        np_freq = np_elt / np_elt.sum()
        entropy = sum([-i * log2(i) for i in np_freq if i != 0])
    return entropy

def plotting(MSA):
    MSA = sys.argv[1]
    entropy_plot = MSA + "_entropy_plot.png"
    
    align = AlignIO.read(MSA, 'fasta')
    length = align.get_alignment_length()
    entropies = []
    for p in range(length):
        bases = list(align[:,p])
        values_count = list(Counter(bases).values())
        entropies.append(entropy(values_count))
    
    X = list(range(len(entropies)))
    
    # Plotting
    plt.figure(figsize=(30, 10), dpi=80, facecolor='w', 
               edgecolor='k')
    plt.title("Entropy from MSA", size = 40)
    plt.xticks(np.arange(0, len(entropies), 1000),size = 30)
    plt.yticks(size=30)
    plt.ylim(-0.1,2.5)
    plt.scatter(X, entropies, s=5, c="black")
    plt.ylabel("Entropy", size = 30)
    plt.xlabel("MSA length", size = 30)
    plt.tight_layout()
    plt.savefig(entropy_plot)
    plt.close()

#==============================================================================
#			       ! ! ! ! !  START OF THE ANALYSIS  ! ! ! ! !
#==============================================================================
if __name__ == "__main__":
    plotting(MSA)

