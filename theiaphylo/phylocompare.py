#! /usr/bin/env python3

import os
import re
import sys
import logging
import argparse
from TheiaPhylo import Phylo
from StdPath import Path

logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(args):
    if args.outgroup:
        outgroup = args.outgroup.split(',')
    else:
        outgroup = []

    # import the trees
    tree1 = Phylo(Path(args.tree1), outgroup = outgroup)
    tree2 = Phylo(Path(args.tree2), outgroup = outgroup)

    # compare the trees
    tree1.compare_trees(tree2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Compare phylogenetic trees')
    parser.add_argument('-t1', '--tree1', required = True, help = 'First tree file')
    parser.add_argument('-t2', '--tree2', required = True, help = 'Second tree file')
    parser.add_argument('-o', '--outgroup', help = 'Comma-delimited list of outgroup tips for rooting trees')
    args = parser.parse_args()

    main(args)
    sys.exit(0)
