#! /usr/bin/env python3

from cogent3 import load_tree, PhyloNode

class RootError(Exception):
    pass

class Phylo(PhyloNode):
    """A class for handling phylogenetic analysis"""
    def __init__(self, tree_path, outgroup = []):
        self.tree = self.import_tree(tree_path)
        if outgroup:
            # root based on outgroup
            self.tree = self.root_tree(outgroup)
        self.root = self.tree.root()

    def import_tree(tree_path):
        """Import a phylogenetic tree"""
        tree = load_tree(tree_path)
        return tree
     
    def root_tree(self, outgroup):
        """Root the tree based on outgroup(s)"""
        if isinstance(outgroup, str) or (isisntance(outgroup, list) and len(outgroup) == 1):
            # root via outgroup tip
            if isinstance(outgroup, list):
                outgroup = outgroup[0]
            self.tree = self.rooted_with_tip(outgroup)
        elif len(outgroup > 1):
            # root by determining the MRCA branch
            nodes = {k: (v, len(v.get_tip_names())) \
                     for k, v in self.tree.get_nodes_dict().items() \
                     if set(outgroup).issubset(set(v.get_tip_names()))}
            mrca_tip_len = min([v[1] for v in list(nodes.values())])
            mrca_edge = [k for k, v in nodes.items() if v[1] == mrca_tip_len]
            try:
                self.tree = self.tree.rooted_at(mrca_edge[0])
            except:
                raise RootError(f'tree could not be rooted with supplied tips: ' \
                     + f'{outgroup}', flush = True)

    def compare_trees(self, tree2, mc = True, rf = True, lrm = True):
        """Quantify tree distances between two phylogenetic trees"""
        mc_dist, rf_dist, lrm_dist = None, None, None
        if self.root and tree2.root:
            # compare rooted trees
            if rf:
                # calculate the Robinson-Foulds distance
                rf_dist = self.tree_distance(tree2, method='rooted_robinson_foulds')
            if mc:
                # calculate the matching cluster distance
                mc_dist = self.tree_distance(tree2, method='matching_cluster')
        elif self.root and not tree2.root:
            raise RootError('cannot compare rooted and unrooted trees')
        elif not self.root and tree2.root:
            raise RootError('cannot compare rooted and unrooted trees')
        else:
            # compare unrooted trees
            if lrm:
                # calculate the least lin rajan moret distance
                lrm_dist = self.tree_distance(tree2, method='lin_rajan_moret')
            if rf:
                # calculate the Robinson-Foulds distance
                rf_dist = self.tree_distance(tree2, method='unrooted_robinson_foulds')
        return mc_dist, rf_dist, lrm_dist