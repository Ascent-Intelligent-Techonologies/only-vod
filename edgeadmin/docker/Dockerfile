ARG BASE_IMG
FROM ${BASE_IMG}


LABEL creator "nishanth"

SHELL ["/bin/bash", "-c"] 

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    apt-get upgrade && \
    apt-get update && \
    apt-get install -y  \
    byacc \
    cmake \
    curl \
    g++ \
    git

RUN apt-get install ffmpeg libsm6 libxext6  -y


WORKDIR /home/data

RUN apt-get update \
    && apt-get install -y build-essential python3.9 wget git \
    && echo "alias python=python3.9" > ~/.bash_aliases \
    && source ~/.bash_aliases \
    && source ~/.bashrc \
    && mkdir -p /home/tools

COPY requirements.txt /home/tools

RUN apt-get update \
    && apt-get install -y python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python3.9 -m pip -q install --no-cache-dir -r /home/tools/requirements.txt