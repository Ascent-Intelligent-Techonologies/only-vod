# Video on Demand pipeline

## Content
- [Video on Demand pipeline](#video-on-demand-pipeline)
  - [Content](#content)
  - [Basic flow](#basic-flow)
  - [Pre requisites](#pre-requisites)
  - [Installation and bringing containers up.](#installation-and-bringing-containers-up)
  - [Registering a new camera](#registering-a-new-camera)
  - [files and details](#files-and-details)
  - [setting up webcam as a cctv camera with rtsp:](#setting-up-webcam-as-a-cctv-camera-with-rtsp)
  - [Basic Debugging checks.](#basic-debugging-checks)
    - [No media found in kinesis video stream](#no-media-found-in-kinesis-video-stream)
      - [references:](#references)


## Basic flow

![](./docs/only_vod-basicflow.jpg)

## Pre requisites

1. Ubuntu 22.04
2. Docker
3. Docker compose
4. aws accesskey and secret key with kinesis video stream policy added.

## Installation and bringing containers up.
1. setting up environment variables.  file path : `./.env` set the following variables
   1. `ACCESSKEY`
   2. `SECRETKEY`
   3. `AWSREGION`

2. run the following command in the `./` folder to build and run docker images. Note : running it first time will take a long time as the images are built from scratch. 
   `docker compose up`

3. To stop the running software run the following command in the `./` folder.
    `docker compose down`

4. To stop any dangling containers we can use the following command.
   `docker stop "ImageId"`

5. For fresh setup always delete `cameras.json` and `config.json` and then do docker compose up.

## Registering a new camera

1. got to `http://localhost:5254/register_camera`
2. give **unique** name to each camera, Note that the stream name will be the same as camera name. TODO : check if the name is not unique raise an error.
3. note the device_id displayed on the page
4. use`camera name` and `device_id` and execute `/turn_on_vod` in `http://localhost:5254/docs` to start streaming.
5.  use`camera name` and `device_id` and execute `/turn_off_vod` in `http://localhost:5254/docs` to stop streaming.

## files and details

1. `./edgefastapi/src/config/cameras.json` -  holds the local settings for all the cameras. Holds the information of the local custom rtsp urls.
2. `./edgefastapi/src/config/config.json`  -  holds the unique device id.


## setting up webcam as a cctv camera with rtsp:

1. `wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.16.0/rtsp-simple-server_v0.16.0_linux_amd64.tar.gz` -- command used to download the simple rtsp server
2. `tar -xzvf rtsp-simple-server_v0.16.0_linux_amd64.tar.gz`--unzip the downloaded file
3. `RTSP_RTSPADDRESS=192.168.XXX.XXX:8554 ./rtsp-simple-server` running the server on the address and port. give machine ip. run this command in the same folder where the unzip command is executed.
   After running the rtsp server, we need to collect the frames from a device and push them on to the server endpont. 
4. `sudo apt-get install v4l-utils` v4l utils is needed to access the media device
5. `sudo v4l2-ctl — list-devices` - this will show all the listed devices and the camera should be /dev/videoX.
6. `sudo ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -c:v libx264 -f rtsp -rtsp_transport tcp rtsp://192.168.XXX.XXX:8554/mystream` push video frames to the rtsp server at /mystream endpoint. Note to make sure you have libx264 -which gives h264 encoding equivalent in cctv. In case there are multiple cameras connected, you have to select the right one and point it as input. /dev/video0 can be /dev/video1 ,...

## Basic Debugging checks.

### No media found in kinesis video stream
![](./docs/Screenshot1.png)
1. check if the rtsp stream is working using vlc player.
2. check if the camera registration was accurate.(check the stream name, url).
3. check the logs of custom rtsp container
4. check the logs of vod container.
5. If all look fine, ssh into the vod container, run the gstreamer command manually to check if the gstreamer or the kinesis video stream is causing any issue.

#### references:
https://kaustavmukherjee-66179.medium.com/convert-any-webcam-into-ipcam-in-2-minutes-using-rtsp-server-and-ffmpeg-a27414f08af5