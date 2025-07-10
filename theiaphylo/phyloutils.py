#! /usr/bin/env python3
"""
Library of functions for phylogenetic tree analysis in Python
"""

import sys
import logging
import argparse
from theiaphylo._version import __version__
from theiaphylo.lib.StdPath import Path
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
    # report if the node is at the root
    if not parent:
        return None, None
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
        if outgroup:
            return tree.rooted_with_tip(outgroup).bifurcating()
        else:
            return tree
    elif outgroup:
        # root by determining the MRCA branch as the MRCA that contains as few tips as possible
        # while including those delineated in the outgroup list
        if len(outgroup) > 2:
            raise RootError(
                "Outgroup must be a list of 1 or 2 tips, or a single tip string."
            )
        mrca = tree.get_connecting_node(outgroup[0], outgroup[1])
        left, right = split_tree(tree, mrca.name)
        if (left, right,) == (None, None,):
            logger.warning("Outgroup(s) have no detectable parent node; rooting on outgroups' MRCA may be erroneous")
            # root on a random tip to then retrieve the other root
            random_tip = sorted(set(tree.get_tip_names()).difference(set(outgroup)))[0]
            tree = root_tree(tree, outgroup=random_tip)
            mrca = tree.get_connecting_node(outgroup[0], outgroup[1])
            left, right = split_tree(tree, mrca.name)
        try:
            return type(tree)(name="root", children=[left, right])
        except:
            raise RootError(
                f"tree could not be rooted with supplied tips: " + f"{outgroup}"
            )


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

def main():
    parser = argparse.ArgumentParser(description="General phylogenetic analysis tools")
    parser.add_argument(
        "tree", type=str, help="Path to the input tree file"
    )
    parser.add_argument(
        "-o", "--outgroup", type=str, help="Comma-delimited outgroup(s) for rooting the tree",
        default = ''
    )
    parser.add_argument(
        "-m", "--midpoint", action="store_true", help="Use midpoint rooting"
    )
    parser.add_argument(
        "-r", "--remove_lengths", action="store_true", help="Remove branch lengths"
    )
    parser.add_argument(
        "--output", type=str, help="Path to the output tree file"
    )
    parser.add_argument(
        "-v", "--version", action="version", version=str(__version__)
    )
    args = parser.parse_args()

    # Incompatible options
    if args.outgroup and args.midpoint:
        raise ValueError("Cannot use both outgroup and midpoint rooting")

    # import the tree
    tree = import_tree(args.tree, outgroup=args.outgroup.split(","), midpoint=args.midpoint)
    logger.info(f"Imported tree:\n{tree.ascii_art()}")

    # output the tree
    if args.output:
        with open(Path(args.output), "w") as f:
            f.write(tree.get_newick(with_distances = not args.remove_lengths))
        logger.info(f"Output tree saved to {args.output}")
    else:
        print(tree.get_newick(with_distances = not args.remove_lengths))

    sys.exit(0)


if __name__ == "__main__":
    main()
