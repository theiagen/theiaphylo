#! /usr/bin/env Rscript

library('ape')

# accept command-line args
args <- commandArgs(trailingOnly = TRUE)

# read tree
tree <- read.tree(args[1])

# convert 0 branches to polytomy
multifurc_tree <- di2multi(tree)

# write tree
out_path <- paste(args[1], "clean", sep = "_")
write.tree(multifurc_tree, out_path)
