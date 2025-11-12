#! /usr/bin/env Rscript

library('phytools')
library('RColorBrewer')

# accept command-line args
args <- commandArgs(trailingOnly = TRUE)

# read trees
tree1 <- read.tree(args[1])
tree2 <- read.tree(args[2])

# get a color palette
n_tips <- length(union(tree1$tip.label, tree2$tip.label))
palette <- colorRampPalette(brewer.pal(n=min(12, n_tips), name="Paired"))(n_tips)
palette <- make.transparent(palette, 0.5)

# generate cophylo plot
cophylo_plot <- cophylo(tree1, tree2)

# plot and save a standard cophylo plot
pdf("cophylo_with_lengths.pdf")
plot(cophylo_plot, link.col=palette, 
     link.lwd=4, link.type="curved",
     link.lty="solid", fsize=c(0.8,0.8),
     main = cat(c(args[1], " v ", args[2])))
dev.off()

# plot and save a no branch length cophylo plot
tree1$edge.length <- NULL
tree2$edge.length <- NULL

# generate cophylo plot
nolength_plot <- cophylo(tree1, tree2)

pdf("cophylo_branch_order.pdf")
plot(nolength_plot, link.type="curved", 
     link.lwd=4, link.col=palette,
     link.lty="solid", fsize=c(0.8,0.8),
     main = cat(c(args[1], " v ", args[2])))
dev.off()

