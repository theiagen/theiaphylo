#! /usr/bin/env Rscript

library('phytools')

# accept command-line args
args <- commandArgs(trailingOnly = TRUE)

# read trees
tree1 <- read.tree(args[1])
tree2 <- read.tree(args[2])

# generate cophylo plot
cophylo_plot <- cophylo(tree1, tree2)

# plot and save
pdf("cophylo_plot.pdf")
plot(cophylo_plot, tip.lty = "solid", link.lwd = 3, link.lty = "solid",
     link.col = make.transparent("black", 0.2), part = 0.3, lwd=3)
dev.off()