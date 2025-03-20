ARG THEIAPHYLO_VER="0.1.0"

FROM google/cloud-sdk:455.0.0-slim 

ARG THEIAPHYLO_VER

RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN "${SHELL}" <(curl -L micro.mamba.pm/install.sh) -y

RUN git clone https://github.com/theiagen/theiaphylo.git \
    && mv theiaphylo /theiaphylo

#RUN wget https://github.com/theiagen/theiavalidate/archive/refs/tags/v${THEIAVALIDATE_VER}.tar.gz \
 #   && tar -xzf v${THEIAVALIDATE_VER}.tar.gz \
  #  && mv theiavalidate-${THEIAVALIDATE_VER} /theiavalidate \
   # && rm v${THEIAVALIDATE_VER}.tar.gz

RUN micromamba env create --name theiaphylo --file /theiaphylo/environment.yml \

RUN echo "micromamba activate theiaphylo" >> ~/.bashrc

ENV PATH="/theiaphylo/theiaphylo:${PATH}"

RUN phylocompare.py -h

WORKDIR /data