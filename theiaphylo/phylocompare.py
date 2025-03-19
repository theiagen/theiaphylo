#! /usr/bin/env python3

import os
import re
import sys
import logging
import argparse
from TheiaPhylo import *
from StdPath import Path


def compare_trees(tree1, tree2, mc = True, rf = True, lrm = True, rooted = True):
    """Quantify tree distances between two phylogenetic trees"""
    mc_dist, rf_dist, lrm_dist = None, None, None
    if rooted:
        # compare rooted trees
        if rf:
            # calculate the Robinson-Foulds distance
            rf_dist = tree1.tree_distance(tree2, method='rooted_robinson_foulds')
        if mc:
            # calculate the matching cluster distance
            mc_dist = tree1.tree_distance(tree2, method='matching_cluster')
    else:
        # compare unrooted trees
        if lrm:
            # calculate the least lin rajan moret distance
            lrm_dist = tree1.tree_distance(tree2, method='lin_rajan_moret')
        if rf:
            # calculate the Robinson-Foulds distance
            rf_dist = tree1.tree_distance(tree2, method='unrooted_robinson_foulds')
    return mc_dist, rf_dist, lrm_dist

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
            # CURRENTLY NOT FUNCTIONAL WITH MULTIPLE OUTGROUPS
            if len(outgroup) > 1:
                raise RootError('multiple outgroups not supported')
    else:
        # CURRENTLY NOT FUNCTIONAL WITHOUT EXPLICIT ROOT
        raise ValueError('no rooting method provided')
    
    # import the trees
    tree1 = import_tree(Path(args.tree1), outgroup = outgroup, midpoint = args.midpoint)
    tree2 = import_tree(Path(args.tree2), outgroup = outgroup, midpoint = args.midpoint)

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
    parser.add_argument('-d', '--debug', action = 'store_true', help = 'Enable debug mode')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level = logging.DEBUG,
                            format = '%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level = logging.INFO,
                            format = '%(asctime)s - %(levelname)s - %(message)s') 
    logger = logging.getLogger(__name__)

    main(args)
    sys.exit(0)
