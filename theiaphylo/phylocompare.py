#! /usr/bin/env python3

import os
import re
import sys
import logging
import argparse
from TheiaPhylo import *
from StdPath import Path

logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def output_results(res_path, tree_res):
    """Output the results of the tree comparison"""
    with open(res_path, 'w') as res_file:
        res_file.write('#robinson_foulds_distance\tmatching_cluster_distance\tlin-rajan-moret_distance\n')
        res_file.write(f'{tree_res[0]}\t{tree_res[1]}\t{tree_res[2]}\n')

def main(args, output_file = 'phylocompare_results.txt'):
    """Main function"""
    outgroup = []
    if args.outgroup and args.midpoint:
        raise ValueError('cannot root trees at midpoint and with outgroup simultaneously')
    elif args.outgroup or args.midpoint:
        rooted = True
        if args.outgroup:
            outgroup = args.outgroup.split(',')
    
    # import the trees
    tree1 = import_tree(Path(args.tree1), outgroup = outgroup, midpoint = args.midpoint)
    tree2 = import_tree(Path(args.tree2), outgroup = outgroup, midpoint = args.midpoint)
    # DETERMINE IF ROOT EXISTS

    # compare the trees
    tree_res = compare_trees(tree1, tree2, rooted = rooted)

    # output the results
    output_results(output_file, tree_res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Compare phylogenetic trees')
    parser.add_argument('-t1', '--tree1', required = True, help = 'First tree file')
    parser.add_argument('-t2', '--tree2', required = True, help = 'Second tree file')
    parser.add_argument('-o', '--outgroup', help = 'Comma-delimited list of outgroup tips for rooting trees')
    parser.add_argument('-m', '--midpoint', action = 'store_true', help = 'Root trees at midpoint')
    args = parser.parse_args()

    main(args)
    sys.exit(0)
