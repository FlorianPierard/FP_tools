#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Florian Pierard

"""
Description = '''This script takes as input a MCC tree from BEAST and generates
a newick tree with the posterior as node label.'''
#==============================================================================
# Import the packages
#==============================================================================
from Bio import Phylo
import os
import json 
import argparse
#==============================================================================
# Functions
#==============================================================================
def mcc_to_nwk(tree_file, output_dir, name):
    newick_file = os.path.join(output_dir, f"{name}_augur.newick")
    json_file = os.path.join(output_dir, f"{name}_augur.json")
    # Run augur
    cmd = ["augur", "import", "beast", "--mcc", tree_file, 
           "--output-tree", newick_file,
           "--output-node-data", json_file]
    str_cmd = " ".join(cmd)
    os.system(str_cmd)
    return newick_file, json_file

def read_json(json_file):
    # Read the json file
    node_posteriors = {}
    with open(json_file) as data_file:
        data = json.load(data_file)
    for node, values_dict in data["nodes"].items():
        if "NODE" in node:
            node_posteriors[node] = values_dict["posterior"]
    return node_posteriors

def add_posteriors_to_nwk(tree_file, json_file):
    node_posteriors = read_json(json_file)
    tree = Phylo.read(tree_file, "newick")
    for clade in tree.find_clades():
        if clade.name in node_posteriors.keys():
            clade.name = str(node_posteriors[clade.name])
    return tree
    
def main(tree_file, output_dir, name):
    final_newick_file = os.path.join(output_dir, f"{name}_posteriors.nwk")
    
    newick_file, json_file = mcc_to_nwk(tree_file, output_dir, name)
    tree = add_posteriors_to_nwk(newick_file, json_file)
    Phylo.write(tree, final_newick_file, "newick")
#==============================================================================
# START
#==============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=Description)
    required_arguments = parser.add_argument_group('Required arguments')
    # Required arguments
    required_arguments.add_argument(
        '-t', metavar = "MCC tree file", required = True, 
        help='Path to your bam file')
    # Optional arguments
    parser.add_argument(
        '-o', metavar = "Output directory",
        help='The output directory where the results will be written')
    parser.add_argument(
        '-n', metavar = "Name", 
        help='Name of your analysis')
    args = parser.parse_args()
    # Import the arguments
    tree_file = args.t
    output_dir = args.o
    name = args.n
    # Check if it exists already
    if output_dir == None:
        output_dir = os.path.dirname(tree_file)
    if name == None:
        name = os.path.basename(tree_file)
    # Start the analysis
    main(tree_file, output_dir,name)
    
