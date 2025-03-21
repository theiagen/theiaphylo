#! /usr/bin/env python3
"""
Library of functions for phylogenetic tree analysis in Python
"""

import logging
from cogent3 import load_tree

logger = logging.getLogger(__name__)


class RootError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def root_tree(tree, outgroup=[], midpoint=False):
    """Root the tree based on outgroup(s)"""
    if midpoint:
        # root at the midpoint
        return tree.root_at_midpoint()
    elif isinstance(outgroup, str) or (
        isinstance(outgroup, list) and len(outgroup) == 1
    ):
        # root via outgroup tip if there is 1 list member or it is a string
        if isinstance(outgroup, list):
            outgroup = outgroup[0]
        return tree.rooted_with_tip(outgroup).bifurcating()
    elif outgroup:
        # root by determining the MRCA branch as the MRCA that contains as few tips as possible
        # while including those delineated in the outgroup list
        nodes = {
            k: (v, len(v.get_tip_names()))
            for k, v in tree.get_nodes_dict().items()
            if set(outgroup).issubset(set(v.get_tip_names()))
        }
        mrca_tip_len = min([v[1] for v in list(nodes.values())])
        mrca_edge = [k for k, v in nodes.items() if v[1] == mrca_tip_len][0]
        try:
            return tree.rooted_at(mrca_edge).bifurcating()
        except:
            raise RootError(
                f"tree could not be rooted with supplied tips: " + f"{outgroup}"
            )
    else:
        raise RootError(f"no outgroup provided")


def import_tree(tree_path, outgroup=[], midpoint=False):
    """Import a phylogenetic tree"""
    tree = load_tree(tree_path)
    if outgroup or midpoint:
        rooted_tree = root_tree(tree, outgroup, midpoint)
        logger.debug(f"Rooted {tree_path}:\n{rooted_tree.ascii_art()}")
        return rooted_tree
    else:
        logger.debug(f"{tree_path}:\n{tree.ascii_art()}")
        return tree
    

def check_root(tree):
    """Check if a tree is rooted"""
    if len(tree.children) != 2:
        return False
    else:
        return True
