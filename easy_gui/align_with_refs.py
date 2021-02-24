#!/usr/bin/env python3

# =============================================================================
# Author: Florian Pierard
# Email: florian.pierard@gmail.com
# =============================================================================
Description = '''This script is made for phylogenetic analysis to differentiate
local outbreak from single introductions events
For questions, please send an email to:
florian.pierard@kuleuven.be'''
# =============================================================================
# Import
# =============================================================================
import os
import sys
import subprocess
import configparser
import argparse
# import phylorigin.functions as ff
#==============================================================================
# Arguments
#=============================================================================
parser = argparse.ArgumentParser(description=Description)
# Required args
parser.add_argument('-c','--config',
    help='Full path to the config file')
parser.add_argument('-f','--fasta',
    help='Full path to the config file')
parser.add_argument('-HCV','--HCV_ON',
    help='''If you want to use the default config for HCV''',
    action="store_true")
args = parser.parse_args()
# Retrieve all arguments
config_file = args.config
# Read the config file
# config_file = "/home/florian/PhylOrigin/configs/HIV_config.ini"

    

"iqtree -s “Alignment_file” -m GTR+G -alrt 1000 -bb 1000 -nt AUTO"




