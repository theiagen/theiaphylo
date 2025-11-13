ARG THEIAPHYLO_VER="0.2.0"

FROM google/cloud-sdk:532.0.0

ARG THEIAPHYLO_VER

RUN apt-get update \
  && apt-get install -y \
    procps wget tzdata \
    python3 python3-pip python3-setuptools python3-wheel \
    r-base-core \
  && rm -rf /var/lib/apt/lists/*

RUN Rscript -e 'install.packages(c("phytools"))'

RUN Rscript -e 'install.packages(c("RColorBrewer"))'

COPY ./ /theiaphylo/

RUN python3 -m pip install /theiaphylo/ --break-system-packages

ENV PATH="/theiaphylo/theiaphylo:${PATH}"

RUN test_dir=/theiaphylo/test/ \
  && phyloutils -v \
  && phylovalidate -v \
  && phylovalidate ${test_dir}tree1.newick ${test_dir}tree2.newick \
      --debug \
  && Rscript theiaphylo/theiaphylo/clean_phylo.R ${test_dir}tree1.newick > ${test_dir}tree1.clean.newick \
  && Rscript theiaphylo/theiaphylo/clean_phylo.R ${test_dir}tree2.newick > ${test_dir}tree2.clean.newick \
  && Rscript theiaphylo/theiaphylo/gen_cophylo.R ${test_dir}tree1.clean.newick ${test_dir}tree2.clean.newick \
  && phyloutils ${test_dir}tree2.clean.newick --outgroup "reference" --output ${test_dir}tree2_rooted.newick \
  && rm -rf /theiaphylo/test cophylo_*.pdf

WORKDIR /data
