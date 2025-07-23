ARG THEIAPHYLO_VER="0.1.7"

FROM mambaorg/micromamba

ARG THEIAPHYLO_VER

USER root

RUN apt-get update \
    && apt-get install -y \
      wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY env.yaml /tmp/env.yaml

RUN micromamba install -y -n base -f /tmp/env.yaml \
    && micromamba clean -a -y 

RUN wget https://github.com/theiagen/theiaphylo/archive/refs/tags/v${THEIAPHYLO_VER}.tar.gz \
    && tar -xzf v${THEIAPHYLO_VER}.tar.gz \
    && mv theiaphylo-${THEIAPHYLO_VER} /theiaphylo \
    && rm v${THEIAPHYLO_VER}.tar.gz

ENV PATH="/theiaphylo/theiaphylo:${PATH}"
ENV PATH="/opt/conda/bin/:${PATH}"

RUN python -m pip install /theiaphylo/

RUN test_dir=/theiaphylo/test/ \
    && phyloutils -v \
    && phylocompare -v \
    && phylocompare ${test_dir}tree1.newick ${test_dir}tree2.newick \
        --debug \
    && phyloutils ${test_dir}tree1.newick --outgroup "reference" --output ${test_dir}tree1_rooted.newick \
    && phyloutils ${test_dir}tree2.newick --outgroup "reference" --output ${test_dir}tree2_rooted.newick \
    && phylocompare ${test_dir}tree1_rooted.newick ${test_dir}tree2_rooted.newick \
        --debug \
    && Rscript theiaphylo/theiaphylo/clean_phylo.R /theiaphylo/test/tree1.newick \
    && rm -rf phylocompare_results.txt /theiaphylo/test

WORKDIR /data