#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Florian Pierard
@date: 04 November 2019
"""
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
# Functions
#==============================================================================
def entropy(list_of_values):
    '''Return the entropy of a list of values. It doesn't count a value if 
    it is less than 5.'''
    Entropy = 0
    np_elt = np.array(list_of_values)
    if not all(np_elt == 0):
        np_freq = np_elt / np_elt.sum()
        Entropy = sum([-i * log2(i) for i in np_freq if i != 0])
    return Entropy

#==============================================================================
# Analysis
#==============================================================================
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

#==============================================================================
# Plotting
#==============================================================================
fig, ax= plt.subplots()
fig.set_size_inches(30,10)
plt.xticks(np.arange(0, len(entropies), 1000),size = 30)
plt.yticks(size=30)
plt.ylim(-0.1,2.5)
plt.scatter(X, entropies, s=5, c="black")
ax.set_ylabel("Entropy", size = 40)
ax.set_xlabel("MSA length", size = 40)
fig.tight_layout()
fig.savefig(entropy_plot)
plt.close()
