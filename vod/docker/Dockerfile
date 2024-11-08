ARG BASE_IMG
FROM ${BASE_IMG}

LABEL creator "harsha"

SHELL ["/bin/bash", "-c"] 

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    apt-get upgrade && \
    apt-get update && \
    apt-get install -y  \
    byacc \
    cmake \
    curl \
    g++ \
    git \
    gstreamer1.0-plugins-base-apps \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    m4 \
    maven \
    openjdk-8-jdk \
    python2.7 \
    pkg-config \
    vim \
    wget  \
    xz-utils && \
    rm -rf /var/lib/apt/lists/* && \
    cd /opt/

# ===== Setup Kinesis Video Streams Producer SDK (CPP) =======================================
WORKDIR /opt/
RUN git clone https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git
WORKDIR /opt/amazon-kinesis-video-streams-producer-sdk-cpp/build/
RUN cmake .. -DBUILD_GSTREAMER_PLUGIN=ON &&\
    make

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/
ENV LD_LIBRARY_PATH=/opt/amazon-kinesis-video-streams-producer-sdk-cpp/open-source/local/lib:$LD_LIBRARY_PATH
ENV GST_PLUGIN_PATH=/opt/amazon-kinesis-video-streams-producer-sdk-cpp/build

# ======= Python dependencies for gRPC server ================================================

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
    && python3.9 -m pip -q install -r /home/tools/requirements.txt

RUN python3.9 -m pip install numpy==1.26.4 opencv-python==4.10.0.84 --no-deps