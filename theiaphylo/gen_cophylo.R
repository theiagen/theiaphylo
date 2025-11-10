#! /usr/bin/env Rscript

library('phytools')

# accept command-line args
args <- commandArgs(trailingOnly = TRUE)

# read trees
tree1 <- read.tree(args[1])
tree2 <- read.tree(args[2])
resolve_discrepancies <- exists("--resolve_tips", where = args)

if (resolve_discrepancies) {
  # get common tips
  symmetric_diff <- setdiff(union(tree1$tip.label, tree2$tip.label),
                            intersect(tree1$tip.label, tree2$tip.label))
  
  # drop tips not in common
  tree1 <- drop.tip(tree1, setdiff(symmetric_diff, tree1$tip.label))
  tree2 <- drop.tip(tree2, setdiff(symmetric_diff, tree2$tip.label))
}

# generate cophylo plot
cophylo_plot <- cophylo(tree1, tree2)

# plot and save
pdf("cophylo_plot.pdf")
plot(cophylo_plot, tip.lty = "solid", link.lwd = 3, link.lty = "solid",
     link.col = make.transparent("black", 0.2), part = 0.3, lwd=3, 
     main = cat(c(args[1], " v ", args[2])))
dev.off()
