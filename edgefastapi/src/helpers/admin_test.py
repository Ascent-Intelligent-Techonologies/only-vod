# import modules
import os
import sys
import time
import logging
import argparse
from pathlib import Path


# add import path
python_grpc_path = Path(__file__).resolve().parents[2] / 'protos/python_grpc'
sys.path.insert(1, str(python_grpc_path))

# import grpc dependencies
import grpc
import edgeadmin_api_pb2_grpc
from edgeadmin_api_pb2 import  *

# load env variables
server_port = str(os.environ['SERVER_PORT'])
server_address = str(os.environ['SERVER_ADDRESS'])

empty = google_dot_protobuf_dot_empty__pb2.Empty()
#   response = stub.NodeConfig(empty)


# setup logging
logging.basicConfig(level=logging.DEBUG)


class EdgeAdminServiceNode():
    """
    edgeadmin service client node
    """
    def __init__(self):
        """
        Class initializer for edgeadmin client
        """
        self.is_grpc_active = False

        # gRPC client
        MAX_MESSAGE_LENGTH = 512 * 1024 * 1024
        self.channel = grpc.insecure_channel(
            server_address + ':' + server_port,
            options=[
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
            ],
        )

        self.stub = None

    def activate_grpc_channel(self):
        """
        Utility function to activate gRPC channel
        """
        try:
            grpc.channel_ready_future(self.channel).result(timeout=1)
            if not self.is_grpc_active:
                self.stub = edgeadmin_api_pb2_grpc.EdgeAdminServiceStub(self.channel)
                time.sleep(1)
                self.is_grpc_active = True
            return True
        except Exception as error:
            logging.error("unable to connect to edge admin service")
            self.is_grpc_active = False
            return False

    def get_rtsp_url(self):
        request = GetRtspUrlMessage()
        request.device_id = os.environ["DEVICE_ID"]
        if self.is_grpc_active:
            result = self.stub.GetRtspUrl(request)
            return True, result
    
    def get_frame(self):
        if self.is_grpc_active:
            result = self.stub.GetFrame()
            return True, result

# initialize the edgeadmin service node
edgeadmin_client = EdgeAdminServiceNode()

# activate the grpc channel
res = edgeadmin_client.activate_grpc_channel()


def get_rtsp_url_grpc(action="get_rtsp_url",urls=""):

    if not res:
        logging.error('Error with gRPC server connection')
        return -1
    result =[]
    if action == "get_rtsp_url" :
        query_success, query_result = edgeadmin_client.get_rtsp_url()
        if query_success:
            for e in query_result.rtsp_urls:
                result.append(e.rtsp_url)
        return query_success, result
    elif action == "get_frame":
        query_status, query_result = edgeadmin_client.get_frame()
        if query_status:
            result = query_result.s3_path
        return query_status, result
    else:
        return 0,result
    
    
