ARG THEIAPHYLO_VER="0.1.8"

FROM google/cloud-sdk:532.0.0

ARG THEIAPHYLO_VER

RUN apt-get update \
  && apt-get install -y \
    procps wget tzdata \
    python3 python3-pip python3-setuptools python3-wheel \
    r-base-core \
  && rm -rf /var/lib/apt/lists/*

RUN Rscript -e 'install.packages("phytools")'

RUN wget https://github.com/theiagen/theiaphylo/archive/refs/tags/v${THEIAPHYLO_VER}.tar.gz \
    && tar -xzf v${THEIAPHYLO_VER}.tar.gz \
    && mv theiaphylo-${THEIAPHYLO_VER} /theiaphylo \
    && rm v${THEIAPHYLO_VER}.tar.gz

RUN python3 -m pip install /theiaphylo/ --break-system-packages

ENV PATH="/theiaphylo/theiaphylo:${PATH}"

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
  && Rscript theiaphylo/theiaphylo/gen_cophylo.R ${test_dir}tree1_rooted.newick ${test_dir}tree1_rooted.newick \
  && rm -rf phylocompare_results.txt /theiaphylo/test cophylo_plot.pdf

WORKDIR /data
