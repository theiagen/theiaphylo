ARG THEIAPHYLO_VER="0.1.7"

FROM google/cloud-sdk:455.0.0-slim 

ARG THEIAPHYLO_VER

RUN apt-get update \
    && apt-get install -y \
      git procps \
      python3 python3-pip python3-setuptools python3-wheel \
      r-base-core \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/theiagen/theiaphylo \
    && python3 -m pip install /theiaphylo/

RUN Rscript -e 'install.packages("ape")'

#RUN wget https://github.com/theiagen/theiavalidate/archive/refs/tags/v${THEIAVALIDATE_VER}.tar.gz \
 #   && tar -xzf v${THEIAVALIDATE_VER}.tar.gz \
  #  && mv theiavalidate-${THEIAVALIDATE_VER} /theiavalidate \
   # && rm v${THEIAVALIDATE_VER}.tar.gz

ENV PATH="/theiaphylo/theiaphylo:${PATH}"

RUN test_dir=/theiaphylo/test/ \
    && theiaphylo -v \
    && phylocompare -v \
    && phylocompare ${test_dir}tree1.newick ${test_dir}tree2.newick \
        --debug \
    && theiaphylo ${test_dir}tree1.newick --outgroup "reference" --output ${test_dir}tree1_rooted.newick \
    && theiaphylo ${test_dir}tree2.newick --outgroup "reference" --output ${test_dir}tree2_rooted.newick \
    && phylocompare ${test_dir}tree1_rooted.newick ${test_dir}tree2_rooted.newick \
        --debug \
    && Rscript theiaphylo/theiaphylo/clean_phylo.R /theiaphylo/test/tree1.newick \
    && rm -rf phylocompare_results.txt /theiaphylo/test

WORKDIR /data
