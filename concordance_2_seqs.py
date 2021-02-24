#!/usr/bin/env python3

# =============================================================================
# Author: Florian Pierard
# Email: florian.pierard@kuleuven.be
# Last update: 05 July 2018
# =============================================================================

Description = '''This script is made to compare 2 consensus sequences. The 2
arguments must be the path to your 2 consensus sequences you need to compare.
It will calculate the concordance between the 2 consensus sequences, the type of
mismatch and the length of the comparison. The output can be redirected to
a csv file. Don't forget to choose your aligner !!!! '''

# =============================================================================
# Import
# ===========================================================================

import sys
import os
from Bio import SeqIO
from Bio import pairwise2

# =============================================================================
# Functions
# =============================================================================
def remove_start_end_gaps(Seq1,Seq2,sliding,threshold):
	if Seq1[:sliding].count("-") > threshold or Seq2[:sliding].count("-") > threshold:
		#remove the start gaps in the 2 sequences
		while Seq1[:sliding].count("-") > threshold or Seq2[:sliding].count("-") > threshold: 
			Seq1 = Seq1[1:]
			Seq2 = Seq2[1:]
		Seq1 = Seq1[threshold:]
		Seq2 = Seq2[threshold:]
	if Seq1[-sliding:].count("-") > threshold or Seq2[-sliding:].count("-") > threshold:
		#remove the end gaps in the 2 sequences
		while Seq1[-sliding:].count("-") > threshold or Seq2[-sliding:].count("-") > threshold:
			Seq1 = Seq1[:-1]
			Seq2 = Seq2[:-1]
		Seq1 = Seq1[:-threshold]
		Seq2 = Seq2[:-threshold]

# =============================================================================
# !!!! CHOOSE YOUR ALIGNER !!!!
# =============================================================================

# Choose between "mafft" or "biopython"
# However biopython seems really slow using local alignment
# So I would advise to use mafft.
# Feel free to change the script if you fnd better parameters for your data
aligner = "mafft"
# aligner = "biopython"

#==============================================================================
# Arguments
#==============================================================================
# Retrieve your 2 sequences
SeqFile1 = sys.argv[1]
SeqFile2 = sys.argv[2]

#==============================================================================
#			 ! ! ! ! !  START  ! ! ! ! !
#==============================================================================

# Write down a reverse dictionnary
IUPAC_reverse_dict = {
		'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T',
		'M':'A,C', 'R':'A,G', 'W':'A,T',
		'S':'C,G', 'Y' : 'C,T', 'K':'G,T', 
		'V':'A,C,G', 'H':'A,C,T', 'D':'A,G,T',
		'B':'C,G,T','N': 'A,C,G,T', '-': '-'}
IUPAC = ['M', 'R','W','S','Y','K','V','H','D','B','N']
	
# =============================================================================
# Align with biopython
# =============================================================================
if aligner == "biopython":
	for record in SeqIO.parse(SeqFile1,"fasta"):
		Seq1 = record.seq.upper()
	for record in SeqIO.parse(SeqFile2,"fasta"):
		Seq2 = record.seq.upper()
		
	Alignment = pairwise2.align.globalxx(Seq1,Seq2)
	AlignSeq1 = Alignment[0][0]
	AlignSeq2 = Alignment[0][1]

# =============================================================================
# Align with mafft
# =============================================================================

if aligner == "mafft":
	AlignedFile = os.path.basename(SeqFile1).split(".fasta")[0]+"-"+os.path.basename(SeqFile2).split(".fasta")[0]
	cat_files_Path = "temp_"+AlignedFile
	sequencers_files = [SeqFile1,SeqFile2]
	with open (cat_files_Path, "w") as d:
		for fname in sequencers_files:
			with open(fname) as infile:
				for line in infile:
					d.write(line)
				d.write("\n")
	os.system("mafft --quiet --nuc --thread 6 --maxiterate 1000 --localpair %s > %s" % (cat_files_Path,AlignedFile))
	os.remove(cat_files_Path)

	Seqs = []
	for record in SeqIO.parse(AlignedFile,"fasta"):
		Seqs.append(record.seq)
	AlignSeq1= Seqs[0].upper()
	AlignSeq2= Seqs[1].upper()
# 	os.remove(AlignedFile)


# =============================================================================
# Calculate the concordance 
# =============================================================================

NormalBases = ["A","C","G","T"]	
match= 0
mismatch = 0 
pure_mismatch = 0
indel = 0
mixture_mismatch = 0


# Clean if there is a lot of gaps at the end or at the start
remove_start_end_gaps(AlignSeq1,AlignSeq2,100,90)
remove_start_end_gaps(AlignSeq1,AlignSeq2,20,17)
# Count the length of the comparison
numberOfBases = len(AlignSeq1)

# Compare the alignment
# Walk through the alignment
while len(AlignSeq1)>0:
	Base1 = AlignSeq1[0]
	Base2 = AlignSeq2[0]
	if Base1 == Base2:
		match += 1 
	else:
		mismatch += 1
		if Base1 == "-" or Base2 == "-":
			indel += 1
		elif Base1 in NormalBases and Base2 in NormalBases:
			pure_mismatch += 1
		else:
			# Check if the IUPAC code has the base of the other consensus
			PotentialBase1= IUPAC_reverse_dict[Base1]
			PotentialBase2= IUPAC_reverse_dict[Base2]
			Mixt = 0
			for b in PotentialBase1:
				if b in PotentialBase2:
					Mixt = 1
			if Mixt == 1:
				mixture_mismatch += 1
			else:
				pure_mismatch += 1
	AlignSeq1 = AlignSeq1[1:]
	AlignSeq2 = AlignSeq2[1:]
concordance = round((100*match / (match + mismatch)),2)

print ("Concordance,Miture,Indel,Pure,Number_of_bases")
print (",".join(str(i) for i in [concordance,mixture_mismatch,indel,pure_mismatch,numberOfBases]))


