#! /usr/bin/env python3
"""
Library of functions for phylogenetic tree analysis in Python
"""

import logging
from cogent3 import load_tree, make_tree

logger = logging.getLogger(__name__)


class RootError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def split_tree(tree, name):
    node = tree.get_node_matching_name(name)
    length = (node.length or 0.0) / 2
    parent = node.parent
    parent.children.remove(node)
    node.parent = None
    left = node.unrooted_deepcopy()
    left.name = f"{name}-L"
    right = parent.unrooted_deepcopy()
    right.name = f"{name}-R"
    left.length = length
    right.length = length
    return left, right


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
        mrca = tree.get_connecting_node(outgroup)
        left, reft = split_tree(tree, mrca.name)
        try:
            return type(tree)(name="root", children=[left, reft])
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
        logger.debug(f"Rooting {tree_path}")
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


def rm_lengths(tree):
    """Remove branch lengths from a tree"""
    newick = tree.get_newick(with_distances = False)
    return make_tree(newick)
