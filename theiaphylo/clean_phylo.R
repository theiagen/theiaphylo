#! /usr/bin/env Rscript

library('ape')

# accept command-line args
args <- commandArgs(trailingOnly = TRUE)

# read tree
tree <- read.tree(args[1])

# convert 0 branches to polytomy
multifurc_tree <- di2multi(tree)

# report if tree is bifurcating
bifurcation <- is.binary(multifurc_tree)
write(paste('bifurcating:', bifurcation), stderr())

# write tree
write.tree(multifurc_tree, stdout())
