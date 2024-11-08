# Image for the compilation of proto files for gRPC services
ARG BASE_IMG
FROM ${BASE_IMG}

LABEL creator "nishanth"

SHELL ["/bin/bash", "-c"]

ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get install -y build-essential python3.9 wget git \
    && echo "alias python=python3.9" > ~/.bash_aliases \
    && source ~/.bash_aliases \ 
    && source ~/.bashrc \
    && mkdir -p /home/tools

COPY requirements.txt /home/tools

RUN apt-get install -y python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python3.9 -m pip -q install --no-cache-dir -r /home/tools/requirements.txt

RUN python3.9 -m pip install numpy==1.26.4 opencv-python==4.10.0.84 --no-deps