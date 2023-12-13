import json
import os


def vod_flag_on(cameraname, device_id):
    with open("src/config/cameras.json","r") as f:
        list_cameras = json.load(f)
    for camera in list_cameras:
        if camera["cameraname"] == cameraname and camera["device_id"] == device_id:
            camera_state = camera
            break
        
    stream_name = camera_state["stream_name"]
    if stream_name:
        if camera_state["vod_flag"] == 0:
            camera_state["vod_flag"] = 1
            with open("src/config/cameras.json","w") as f:
                json.dump(list_cameras,f)
        return stream_name
    else:
        raise Exception("Stream name not found")
    
    

def vod_flag_off(cameraname,device_id):
    with open("src/config/cameras.json","r") as f:
        list_cameras = json.load(f)
    for camera in list_cameras:
        if camera["cameraname"] == cameraname and camera["device_id"] == device_id:
            camera_state = camera
            break
    stream_name = camera_state["stream_name"]
    if stream_name:
        if camera_state["vod_flag"] == 1:
            camera_state["vod_flag"] = 0
            with open("src/config/cameras.json","w") as f:
                json.dump(list_cameras,f)
        return stream_name
    else:
        raise Exception("Stream name not found")