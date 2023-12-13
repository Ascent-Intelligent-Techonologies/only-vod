import json
import uvicorn
import logging
import requests
from datetime import datetime, timedelta
from uuid import uuid4
from helpers.admin_test import *
from helpers.vod_client import *
from helpers.custom_rtsp import *
from helpers.schemas import *
from helpers.utils import *
from helpers.kvs import *
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException,Request,Form

logger = logging.getLogger(__name__) 

app = FastAPI()

EDGEFASTAPI_PORT = int(os.environ["EDGEFASTAPI_PORT"])

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/admin/get_rtsp_urls", response_model = list[str],  tags=["Admin"])
def get_rtsp_urls():
    status,result = get_rtsp_url_grpc()

    return result



@app.get("/register_camera",response_class=HTMLResponse,tags=["camera"])
def get_register_camera(request:Request):
    """Endpoint to handle registering new camera 
    """
    device_id = os.environ["DEVICE_ID"]
    return templates.TemplateResponse("register_camera.html", {"request": request, "device_id": device_id})


@app.post("/register_camera", tags=["camera"])
def post_register_camera(rtsp_url:str=Form(),cameraname:str=Form(),area:str=Form(),
                        location:str=Form(),district:str=Form(),city:str=Form(),pincode:str=Form(),
                        state:str=Form(),class_name:str=Form(),device_id:str=Form()):
    camera_id = cameraname

    # create a new stream and assign it to this camera
    
    port = 50001
    
    while is_port_available(port) is False:
        port+=1
    
    create_new_rtsp_server(cameraname,rtsp_url,port)
    resp = kinesis_helper.create(camera_id)
    if resp.get("ResponseMetadata").get("HTTPStatusCode") == 200:
        stream_name = camera_id
    else:
        logger.Error(resp)
        raise Exception("Stream creation failed")
    body = json.dumps({
            "cameraname": cameraname,
            "device_id": device_id,
            "area": area,
            "location": location,
            "district": district,
            "city": city,
            "pincode": pincode,
            "state": state,
            "rtsp": rtsp_url,
            "vod_flag": 0,
            "stream_name": stream_name,
            "custom_rtsp": f"""rtsp://127.0.0.1:{port}/stream"""
    })
    try:
        with open("src/config/cameras.json","r") as f:
            list_cameras = json.load(f)
    except:
        # create a new file
        list_cameras= []
    list_cameras.append(json.loads(body))
    with open("src/config/cameras.json", "w") as outfile:
        json.dump(list_cameras,outfile)
    return "sucessesfully registered camera"



@app.get("/camera_details",tags=["camera"])
def get_camera_details(rtsp_url :str):
    logger.info(rtsp_url)
    with open("src/config/cameras.json","r") as f:
        list_cameras = json.load(f)
    for each in list_cameras: 
        if each["rtsp"] == rtsp_url or each["custom_rtsp"] == rtsp_url:
            return each
    else:
        return HTTPException(status_code = 400,detail="unknown rtsp url")

@app.post("/turn_on_vod", response_model=str, tags=["video"])
def turn_vod_flag_on_ep(request: Request, body: cameraBody):
    """endpoint to turn on video on demand flag for a camera"""
    stream_name = vod_flag_on(body.camera_name, body.device_id)
    return stream_name


@app.post("/turn_off_vod", response_model=str, tags=["video"])
def turn_vod_flag_off_ep(request: Request, body: cameraBody):
    """endpoint to turn off video on demand flag for a camera"""
    stream_name = vod_flag_off(body.camera_name, body.device_id)
    return stream_name



@app.post("/delete_camera",tags=["camera"])
def delete_camera_ep(rtsp_url):
    """Endpoint to delete a camera which is already registered

    Args:
        rtsp_url (_type_): _description_

    Returns:
        _type_: _description_
    """
    pass


logging.getLogger("urllib3").setLevel(logging.WARNING)

@app.on_event("startup")
@repeat_every(seconds=1)  # 2seconds
def get_device_state():
    """Do this task every 2 seconds
    get the status of all the cameras attached to this device
    """
    DEVICE_ID = os.environ["DEVICE_ID"]
    with open("src/config/cameras.json","r") as f:
        list_cameras = json.load(f)
    
        
    # All keys available for a camera
    # ['cameraname', 'device_id', 'area', 'location', 'district', 'city', 'pincode', 'state', 'class_name',
    # 's3_path', 'coordsid', 'rtsp', 'vod_flag', 'panic_flag', 'updateml_flag', 'id']

    for camera in list_cameras:
        
        if camera["vod_flag"] == 1:
            # send vodflag on vod grpc
            logger.info("Vod turned on for "+str(camera["cameraname"] ))
            start_vod(stream_name= camera["stream_name"] ,rtsp_url=camera["rtsp"])
        elif camera["vod_flag"] == 0:
            # send vodflag off to vod grpc
            stop_vod(rtsp_url=camera["rtsp"])


    

@app.on_event("startup")
async def startup_event():
    """Function to be run during startup, setups a device-id if it doesntexist
    """
    try :
        with open("src/config/config.json","r") as f:
            conf = json.load(f)
        DEVICE_ID = conf["DEVICE_ID"]
    except Exception as e:
        logger.info(e)
        DEVICE_ID = str(uuid4())
        conf={}
        conf["DEVICE_ID"] = DEVICE_ID
        with open("src/config/config.json", "w") as outfile:
            json.dump(conf,outfile)
    os.environ["DEVICE_ID"] = DEVICE_ID
    logger.info("This Device ID is"+DEVICE_ID)
    
    try:
        if not os.path.exists("src/config/cam_schedule.json"):
            with open("src/config/cam_schedule.json", "w") as outfile:
                json.dump([],outfile)
        if not os.path.exists("src/config/cameras.json"):
            with open("src/config/cameras.json","w") as outfile:
                json.dump([],outfile)

    except Exception as e:   
        logging.error(e)
    
    #Starting custom RTSP Cameras
    try:
        with open("src/config/cameras.json","r") as f:
            list_cameras = json.load(f)
            for each in list_cameras:
                custom_rtsp = each["custom_rtsp"]
                port = int(custom_rtsp.split(":")[2].split("/")[0])
                create_new_rtsp_server(each["cameraname"],each["rtsp"],port)
    except Exception as e:
        logging.error(e)
        logging.info("No custom RTSP feeds started.")

    
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=EDGEFASTAPI_PORT, reload=True)
