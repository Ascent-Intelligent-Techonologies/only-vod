# Video on Demand Module for Camonitor Edge

**Group/Product Name**: 

This repo implements the VOD module on Camonitor Edge which streams a RTSP feed to Amazon Kinesis.

## Table of Contents
* Installation Instructions
* Usage Instructions
* Troubleshooting

## Installation Instructions
This repository has docker support and does not require any system-level dependencies to be installed except for docker specific tools.
* Following are some of the prerequisites:
  * It is prefered to test the working of this repository in Linux OS (preferably Ubuntu).
  * (Optional) Please use a compute device with NVidia GPU. Device could either be something like Jetson Nano or a regular desktop with NVidia GPU card.
  * (Optional) OS should have an NVidia device driver installed. Please run the command `nvidia-smi` and check whether the output provides details about the onboard GPU device.
* Please setup the following to use this repository:
  * Install Docker engine by following the instructions in this [link](https://docs.docker.com/get-docker/). Instructions will depend on the OS in the host machine.
  * Install docker-compose utility by following the instructions in this [link](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html). Instructions will depend on the OS in the host machine.
  * (Optional) Install nvidia-docker utility to provide GPU device access to docker containers by following the instructions in this [link](https://docs.docker.com/compose/install/). Instructions will depend on the OS in the host machine.
* To clone the submodule code, run the following command:
  ```
  $ git submodule update --init
  ```

## Usage Instructions
* Create a `.env` file in the root folder of the repository for docker compose variables as shown below:
  ```
  PRJ_HOME=./
  PRJ_PATH=/home/data
  VOD_BASE_IMAGE=ubuntu:20.04
  
  SERVER_PORT=60003
  SERVER_ADDRESS=127.0.0.1
  ```
* Build the docker container for this repository by running the following command:
  ```
  $ sudo docker compose build
  ```
    This should create a docker image with the tag `camonitor-edge:vod-api`.
* Create a file named `env.sh` for exporting AWS credentials in the following format:
  ```
  export ACCESSKEY=YOUR_ACCESS_KEY
  export SECRETKEY=YOUR_SECRET_KEY
  export AWSREGION=YOUR_AWS_REGION
  ```
* Run the docker container and start the VOD API service by running the following command:
  ```
  $ sudo docker compose up
  ```
  This should start a docker container with the tag `camonitor-vod_vod-server_1`. On starting the container, the shell script `scripts/run_server.sh` would be run to run the `src/vod_server.py` gRPC service.
* To test the gRPC service, we can do the following steps:
  * Attach to the `vod-api` docker container by running the following command:
    ```
    $ docker exec -it camonitor-vod_vod-server_1 /bin/bash
    ```
  * Run the `run_client.sh` shell script to test the working of the vod API service:
    ```
    $ cd /home/data
    $ bash scripts/start_client.sh SERVICE_NAME [...SERVICE_PARAMETERS]
    ```
    where `SERVICE_NAME` can be replaced by services such as `start`, `stop`, `healthcheck` and `status`.
  * Run the following command to get more information about command line arguments for the script:
    ```
    $ bash scripts/run_client.py --help
    ```
  * The following example shows using the `healthcheck` RPC with the `run_client.sh` script:
    ```
    $ bash scripts/run_client.sh healthcheck rtsp://192.168.151.50:8554/mystream1,rtsp://192.168.151.50:8554/mystream2
    ```
## Troubleshooting


