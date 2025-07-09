#! /usr/bin/env python3

import sys
import logging
import argparse
from theiaphylo.phyloutils import *
from theiaphylo.lib.StdPath import Path
from theiaphylo._version import __version__


def compare_trees(tree1, tree2, mc=True, rf=True, lrm=True, rooted=True):
    """Quantify tree distances between two phylogenetic trees"""
    mc_dist, rf_dist, lrm_dist = None, None, None
    if rooted:
        # compare rooted trees
        if rf:
            # calculate the Robinson-Foulds distance
            rf_dist = tree1.tree_distance(tree2, method="rooted_robinson_foulds")
        if mc:
            # calculate the matching cluster distance
            mc_dist = tree1.tree_distance(tree2, method="matching_cluster")
        return rf_dist, mc_dist
    else:
        # compare unrooted trees
        if lrm:
            # calculate the least lin rajan moret distance
            lrm_dist = tree1.tree_distance(tree2, method="lin_rajan_moret")
        if rf:
            # calculate the Robinson-Foulds distance
            rf_dist = tree1.tree_distance(tree2, method="unrooted_robinson_foulds")
        return rf_dist, lrm_dist


def output_results(res_path, tree_res, rooted=False):
    """Output the results of the tree comparison"""
    with open(res_path, "w") as res_file:
        if rooted:
            res_file.write("#rooted_robinson_foulds\tmatching_cluster\n")
        else:
            res_file.write("#unrooted_robinson_foulds\tlin-rajan-moret\n")
        res_file.write(f"{tree_res[0]}\t{tree_res[1]}\n")


def run(args, output_file="phylo_distances.txt"):
    """Main function"""

    # import the trees
    tree1 = import_tree(Path(args.tree1))
    tree2 = import_tree(Path(args.tree2))

    tree1_isrooted = check_root(tree1)
    tree2_isrooted = check_root(tree2)
    if tree1_isrooted != tree2_isrooted:
        raise RootError(
            f"{args.tree1} rooted: {tree1_isrooted}; {args.tree2} rooted: {tree2_isrooted}"
        )
    elif tree1_isrooted:
        rooted = True
    else:
        rooted = False

    logger.debug(f"Trees are rooted: {tree1_isrooted}")

    # compare the trees
    try:
        tree_res = compare_trees(
            tree1,
            tree2,
            rooted=rooted,
            mc=args.matching_cluster,
            rf=args.robinson_foulds,
            lrm=args.lin_rajan_moret,
        )
    except Exception as e:
        logger.error(f"Error comparing trees: {e}")
        tree1_tips = set(tree1.get_tip_names())
        tree2_tips = set(tree2.get_tip_names())
        if tree1_tips != tree2_tips:
            logger.error(
                f"Tips are discrepant: {tree1_tips.symmetric_difference(tree2_tips)}"
            )
        else:
            logger.error(
                "Number of nodes differ: check for polytomies or rooting discrepancies"
            )
        tree_res = (None, None)

    # output the results
    output_results(output_file, tree_res, rooted=rooted)


def main():
    parser = argparse.ArgumentParser(
        description="Compare phylogenetic trees by distance metrics: "
        + "Robinson-Foulds, Matching Cluster, and Lin-Rajan-Moret"
    )
    in_args = parser.add_argument_group("Inputs")
    in_args.add_argument("tree1", help="First tree file")
    in_args.add_argument("tree2", help="Second tree file")

    phy_args = parser.add_argument_group("Distance Options")
    phy_args.add_argument(
        "-mc",
        "--matching_cluster",
        action="store_true",
        help="Calculate matching cluster distance (rooted only); overwrites default: ALL",
    )
    phy_args.add_argument(
        "-rf",
        "--robinson_foulds",
        action="store_true",
        help="Calculate Robinson-Foulds distance; overwrites default: ALL",
    )
    phy_args.add_argument(
        "-lrm",
        "--lin_rajan_moret",
        action="store_true",
        help="Calculate Lin-Rajan-Moret distance (unrooted only); overwrites default: ALL",
    )

    run_args = parser.add_argument_group("Run Options")
    run_args.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug mode"
    )
    run_args.add_argument("-v", "--version", action="version", version=str(__version__))

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    logger = logging.getLogger(__name__)

    # run all comparisons by default
    if (
        not args.matching_cluster
        and not args.robinson_foulds
        and not args.lin_rajan_moret
    ):
        args.matching_cluster = True
        args.robinson_foulds = True
        args.lin_rajan_moret = True

    run(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
