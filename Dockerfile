ARG THEIAPHYLO_VER="0.1.1"

FROM google/cloud-sdk:455.0.0-slim 

ARG THEIAPHYLO_VER

RUN apt-get update \
    && apt-get install -y \
      git procps \
      python3 python3-pip python3-setuptools python3-wheel \
      r-base-core \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install cogent3 

RUN Rscript -e 'install.packages("ape")'

RUN git clone https://github.com/theiagen/theiaphylo.git

#RUN wget https://github.com/theiagen/theiavalidate/archive/refs/tags/v${THEIAVALIDATE_VER}.tar.gz \
 #   && tar -xzf v${THEIAVALIDATE_VER}.tar.gz \
  #  && mv theiavalidate-${THEIAVALIDATE_VER} /theiavalidate \
   # && rm v${THEIAVALIDATE_VER}.tar.gz

ENV PATH="/theiaphylo/theiaphylo:${PATH}"

RUN test_dir=/theiaphylo/test/ \
    && TheiaPhylo.py -v \
    && phylocompare.py -v \
    && phylocompare.py ${test_dir}tree1.newick ${test_dir}tree2.newick \
        --debug \
    && TheiaPhylo.py ${test_dir}tree1.newick --outgroup "reference" --output ${test_dir}tree1_rooted.newick \
    && TheiaPhylo.py ${test_dir}tree2.newick --outgroup "reference" --output ${test_dir}tree2_rooted.newick \
    && phylocompare.py ${test_dir}tree1_rooted.newick ${test_dir}tree2_rooted.newick \
        --debug \
    && Rscript theiaphylo/theiaphylo/clean_phylo.R /theiaphylo/test/tree1.newick \
    && rm -rf phylocompare_results.txt /theiaphylo/test

WORKDIR /data
