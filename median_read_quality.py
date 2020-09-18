#!/usr/bin/env python3

# =============================================================================
# Author: Florian Pierard
# Email: florian.pierard@kuleuven.be
# Last update: 05 July 2018
# =============================================================================
# Write down here a little description of your algorithm. 

Description = '''This script needs as input a directory with all yhe fastq
files that you want to analyse. It will create a csv file for each fastq
with the average quality of each reads with its IQR in a directory named
ReadQuality in the same directory as your fastq files'''

# =============================================================================
# Import
# =============================================================================

import os
import sys
from Bio import SeqIO
import pandas as pd
import numpy as np

#==============================================================================
# Arguments
#==============================================================================
# Retrieve the directory with all the fastq's
FastqDir = sys.argv[1]

#==============================================================================
#			 ! ! ! ! !  START  ! ! ! ! !
#==============================================================================

FastqFileList = [f for f in os.listdir(FastqDir) if f.endswith(".fastq")]

OutputDir = os.path.join(FastqDir,ReadQuality)
os.makedirs(OutputDir) # make the output directory

for fastq in FastqFileList:
	Name= (fastq.split(".fastq")[0])
	print (Name)
	FilePath = os.path.join(FastqDir,fastq)
	df = pd.DataFrame()
	OutputDf = os.path.join(OutputDir,Name+".csv")
	DictDf = {}
	for record in SeqIO.parse(FilePath,"fastq"):
		QualityList = record.letter_annotations["phred_quality"]
		ReadName = record.id
		q75, q25 = np.percentile(QualityList, [75 ,25])
		median = np.median(QualityList)
		df.at[ReadName,"Quality median"] = median
		df.at[ReadName,"Q25"] = q25
		df.at[ReadName,"Q75"] = q75
	df.to_csv(OutputDf,index=True)
