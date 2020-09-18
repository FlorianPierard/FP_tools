#!/usr/bin/env python3

# =============================================================================
# Author: Florian Pierard
# Email: florian.pierard@gmail.com
# Last update: 17 September 2020
# =============================================================================

Description = '''This script will create a coverage plot of a bam file. The 
bam file should be the first argument and the output image the second argument'''

# =============================================================================
# Import
# =============================================================================

import matplotlib.pyplot as plt
import pysam
import sys
import numpy as np

#==============================================================================
# Arguments
#==============================================================================

bamfile = sys.argv[1] # Bam file path
ImageOutput = sys.argv[2] # Output picture that will be created

#==============================================================================
#			 ! ! ! ! !  START  ! ! ! ! !
#==============================================================================
# This line is needed if you want to run it in SSH
plt.switch_backend('agg')

name = (bamfile.split(".bam")[0])

samfile = pysam.Samfile(bamfile, "rb" )
samfile.pileup(max_depth = 1000000)
X = []
for pileupcolumn in samfile.pileup(max_depth=1000000):      
     X.append(pileupcolumn.n)
Y = range(len(X))

# Create the plot
fig, ax= plt.subplots()
# Et up the size of the plot
fig.set_size_inches(30,10)
ax.set_title("Coverage of %s" % name,size = 40)
plt.xticks(np.arange(0, len(X), 1000),size = 20)
plt.yticks(size=20)
plt.plot(Y,X)
# Ad a line to show an eventual threshold
plt.axhline(y=5000, color='r', linestyle='--')
ax.set_ylabel("Coverage",size = 30)
ax.set_xlabel("Genome position",size = 30)
fig.tight_layout()
fig.savefig(ImageOutput)
