# Camonitor Edge Software Protos

**Group/Product Name**: 

This repo contains the proto file definitions for the edge device software of the Camonitor product

## Table of Contents
* Repository Structure
* Installation Instructions
* Usage Instructions
* Troubleshooting

## Repository Structure
Following is the structure of the repository:
```
.
├── docker
├── protos
├── python_grpc
├── scripts
├── README.md
├── .env
├── docker-compose.yml
├── requirements.txt
```

## Installation Instructions

#### [Important] After cloning this repo, run the following command inside root folder to use commit message check.
```
$ git config --local core.hooksPath .github/.githooks/
```
This repository has docker support and does not require any system-level dependencies to be installed except for docker specific tools.
* Following are some of the prerequisites:
  * It is prefered to test the working of this repository in Linux OS (preferably Ubuntu).
  * (Optional) Please use a compute device with NVidia GPU. Device could either be something like Jetson Nano or a regular desktop with NVidia GPU card.
  * (Optional) OS should have an NVidia device driver installed. Please run the command `nvidia-smi` and check whether the output provides details about the onboard GPU device.
* Please setup the following to use this repository:
  * Install Docker engine by following the instructions in this [link](https://docs.docker.com/get-docker/). Instructions will depend on the OS in the host machine.
  * Install docker-compose utility by following the instructions in this [link](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html). Instructions will depend on the OS in the host machine.
  * (Optional) Install nvidia-docker utility to provide GPU device access to docker containers by following the instructions in this [link](https://docs.docker.com/compose/install/). Instructions will depend on the OS in the host machine.

## Usage Instructions
* Build the docker container for this repository by running the following command:
  ```
  $ sudo docker compose build
  ```
  This should create a docker image with the tag `camonitor-edge:protos-service`.
* Run the docker container and build python and Golang libraries for the protos file by running the following command:
  ```
  $ sudo docker compose up
  ```
  This should start a docker container with the tag `camonitor-edgeprotos-server-1`. On starting the container, the shell script `scripts/make_proto.sh` would be run to build the libraries for all the protos files in the `protos` folder and creates the output python dependencies using `python_grpc` folder.
* To use this repository: 
  * It should be included as a submodule in the main service repository.
  * The `python_grpc` folder should be referenced to create a gRPC service corresponding to the proto file defined in the `protos` folder.
* To update this repository:
  * The developer should either create a new `.proto` file inside the `protos` directory or edit an existing `.proto` file.
  * For adding these changes to the repo, make a commit with message having a prefix `CAM-xxx` corresponding to the ticket number on the JIRA board.
  * Run `docker compose up` to recreate the python libraries for local testing.
  * Be sure not to commit these python stubs/libraries to the repo as these will be automatically generated from the CI pipeline.
  * Update reference to the submodule in the main service repository to use the updated definition of the service proto file.
  
## CI Pipeline
* Any new Pull request to the develop branch will trigger a CI pipeline.
* This CI pipeline will check for syntax problems in the .proto files.
* If the proto files are valid, Github actions bot will automatically generate stubs for it and push a commit with these stubs to the pull request.
* If you want to make subsequent changes, make sure you pull these commits from the Github actions bot before pushing anything from your local repo.  

## Troubleshooting
* If you get an error of commit message while commiting changes locally, make sure your commit message has a prefix `CAM-xxx` corresponding to the ticket number.
* If your CI job fails, go to the Actions tab on the repository page to see the logs for your particular run.
* Make sure to pull changes from the Github actions bot when you modify a PR. If you skip this, your push to the remote repository will be rejected.


