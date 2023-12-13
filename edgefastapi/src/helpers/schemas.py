from pydantic import BaseModel, Field, validator
from typing import List, Union, Optional



class cameraBody(BaseModel):
    camera_name: str
    device_id: str


class KVSStreamName(BaseModel):
    stream_name: str

class KVSStreamARN(BaseModel):
    stream_arn: str