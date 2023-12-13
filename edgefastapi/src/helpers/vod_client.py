# import modules
import os
import sys
import time
import logging
import argparse
from pathlib import Path

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

# add import path
python_grpc_path = Path(__file__).resolve().parents[2] / 'protos/python_grpc'
sys.path.insert(1, str(python_grpc_path))

# import grpc dependencies
import grpc
import vod_api_pb2_grpc
from vod_api_pb2 import VODStartMessage, VODStopMessage, RtspUrlMessage

# load env variables
vod_server_port = str(os.environ['VOD_SERVER_PORT'])
server_address = str(os.environ['SERVER_ADDRESS'])
logging.info(vod_server_port)
logging.info(server_address)


class VODServiceNode():
    """
    vod service client node
    """
    def __init__(self):
        """
        Class initializer for vod client
        """
        self.is_grpc_active = False

        # gRPC client
        MAX_MESSAGE_LENGTH = 512 * 1024 * 1024
        self.channel = grpc.insecure_channel(
            server_address + ':' + vod_server_port,
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
            logger.info(str(self.is_grpc_active))
            if not self.is_grpc_active:
                time.sleep(1)
                self.stub = vod_api_pb2_grpc.VODServiceStub(self.channel)
                self.is_grpc_active = True
            return True
        except Exception as error:
            logging.info("Unable to connect to vod service grpc")
            logging.error(str(error))
            self.is_grpc_active = False
            return False

    def start_vod(self,stream_name,rtsp_url):
        """
        Utility function to start vod by calling StartVOD rpc
        :param stream_name: Name of the Kinesis stream
        :param rtsp_url: RTSP URL for the camera feed
        """
        if self.is_grpc_active:
            # initialize request message
            request = VODStartMessage()
            request.stream_name = stream_name
            request.rtsp_url = rtsp_url

            # call the rpc
            result = self.stub.StartVOD(request)

            return True, result
        else:
            return False, 'gRPC channel is inactive'
    
    def stop_vod(self,rtsp_url):
        """
        Utility function to stop vod by calling StopVOD rpc
        :param rtsp_url: RTSP URL for the camera feed
        """
        if self.is_grpc_active:
            # initialize request message
            request = VODStopMessage()
            request.rtsp_url = rtsp_url

            # call the rpc
            result = self.stub.StopVOD(request)

            return True, result
        else:
            return False, 'gRPC channel is inactive'
    

# initialize the vod service node
vod_client = VODServiceNode()

# activate the grpc channel
res = vod_client.activate_grpc_channel()


def start_vod(stream_name,rtsp_url):
    
    if not res:
        logger.error('Error with gRPC server connection')
        return -1
    

    query_success, query_result = vod_client.start_vod(stream_name,rtsp_url)

    if query_success and query_result.success:
        logger.info("Start VOD RPC Call successful")
        logger.info(query_result.status_message)
    else:
        logger.error("Error in starting VOD")
        logger.error(query_result.status_message)
    
    return query_result.status_message


def stop_vod(rtsp_url):
    
    if not res:
        logger.error('Error with gRPC server connection')
        return -1
    
    query_success, query_result = vod_client.stop_vod(rtsp_url)

    if query_success and query_result.success:
        logger.info(query_result.status_message)
    else:
        logger.error("Error in stopping VOD")
        logger.error(query_result.status_message)

    return query_result.status_message


    

