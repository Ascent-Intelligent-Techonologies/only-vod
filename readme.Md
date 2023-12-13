
## setting up webcam as a cctv camera with rtsp:

1. `wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.16.0/rtsp-simple-server_v0.16.0_linux_amd64.tar.gz` download rtsp server 
2. `tar -xzvf rtsp-simple-server_v0.16.0_linux_amd64.tar.gz` unzip
3. `RTSP_RTSPADDRESS=192.168.XXX.XXX:8554 ./rtsp-simple-server` running the server on the address and port. give machine ip
4. `sudo apt-get install v4l-utils` v41 utils
5. `sudo v4l2-ctl — list-devices` list devices
6. `sudo ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -c:v libx264 -f rtsp -rtsp_transport tcp rtsp://192.168.1.71:8554/mystream` push video frames to the rtsp server at /mystream endpoint. Note to make sure you have libx264 -which gives h264 encoding equivalent in cctv.




#### references:
https://kaustavmukherjee-66179.medium.com/convert-any-webcam-into-ipcam-in-2-minutes-using-rtsp-server-and-ffmpeg-a27414f08af5