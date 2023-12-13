"""
============================================================================
# Name        : vod_client.py
# Description : VOD service client to test functionality of vod service
============================================================================
"""

# import modules
import os
import sys
import time
import logging
import argparse
from pathlib import Path


# add import path
python_grpc_path = Path(__file__).resolve().parents[1] / 'protos/python_grpc'
sys.path.insert(1, str(python_grpc_path))

# import grpc dependencies
import grpc
import vod_api_pb2_grpc
from vod_api_pb2 import VODStartMessage, VODStopMessage, VODStatusMessage, HealthCheckMessage, RtspUrlMessage

# load env variables
server_port = str(os.environ['SERVER_PORT'])
server_address = str(os.environ['SERVER_ADDRESS'])


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
                self.stub = vod_api_pb2_grpc.VODServiceStub(self.channel)
                time.sleep(5)
                self.is_grpc_active = True
            return True
        except Exception as error:
            logging.error(error)
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
    
    def check_vod_status(self,stream_name,rtsp_url):
        """
        Utility function to check status of vod by calling CheckVODStatus rpc
        :param stream_name: Name of the AWS Kinesis stream
        """
        if self.is_grpc_active:
            # initialize request message
            request = VODStatusMessage()
            request.stream_name = stream_name
            request.rtsp_url = rtsp_url

            # call the rpc
            result = self.stub.CheckVODStatus(request)

            return True, result
        else:
            return False, 'gRPC channel is inactive'

    def health_check(self,rtsp_urls):
        """
        Utility function to call terminate camera rpc
        :param config: Config dictionary with request details
        """
        if self.is_grpc_active:
            # initialize request message
            request = HealthCheckMessage()

            for rtsp_url in rtsp_urls:
                rtsp_url_message = RtspUrlMessage()
                rtsp_url_message.rtsp_url = rtsp_url
                request.rtsp_urls.append(rtsp_url_message)

            # call the rpc
            result = self.stub.HealthCheck(request)

            return True, result
        else:
            return False, 'gRPC channel is inactive'


def main():
    """
    Main function for vod service client
    """
    parser = argparse.ArgumentParser(
        description='Client for VOD service')
    parser.add_argument(
        'service', type=str,
        help='Service to use for VOD client',
        choices=["start","stop","healthcheck","status"])
    parser.add_argument(
        'service_arg_1', type=str,
        help='''Argument 1 for the service.
        For start service: AWS Kinesis Stream Name.
        For stop service: RTSP URL of the camera feed. 
        For heathcheck service: Comma separated list of RTSP URLs.
        For status service: AWS Kinesis Stream Name.''',
    )
    parser.add_argument(
        'service_arg_2',nargs='?',type=str,
        help='''Argument 2 for the service.
        For start service: RTSP URL of the camera feed.
        For status service: RTSP URL of the camera feed
        '''
    )

    args = parser.parse_args()

    # setup logging
    logging.basicConfig(level=logging.DEBUG)
    
    # initialize the vod service node
    vod_client = VODServiceNode()

    # activate the grpc channel
    res = vod_client.activate_grpc_channel()

    if not res:
        logging.error('Error with gRPC server connection')
        return -1
    
    if args.service == "start":
        stream_name = args.service_arg_1
        rtsp_url = args.service_arg_2
        query_success, query_result = vod_client.start_vod(stream_name,rtsp_url)

        if query_success and query_result.success:
            logging.info("Start VOD RPC Call successful")
            logging.info(query_result.status_message)
        else:
            logging.error("Error in starting VOD")
            logging.error(query_result.status_message)
    
    elif args.service == "stop":
        rtsp_url = args.service_arg_1
        query_success, query_result = vod_client.stop_vod(rtsp_url)

        if query_success and query_result.success:
            logging.info(query_result.status_message)
        else:
            logging.error("Error in stopping VOD")
            logging.error(query_result.status_message)

    elif args.service == "healthcheck":

        rtsp_urls = args.service_arg_1.split(",")

        query_success, query_result = vod_client.health_check(rtsp_urls)
        if query_success and query_result.success:
            logging.info("Health Check RPC call successful")
            for feed_health in query_result.feeds:
                logging.info(feed_health.status_message)
        else:
            logging.error("Error in health check RPC call")
            logging.error(query_result.status_message)
    
    elif args.service == "status":
        
        stream_name = args.service_arg_1
        rtsp_url = args.service_arg_2
        query_success, query_result = vod_client.check_vod_status(stream_name,rtsp_url)
        if query_success and query_result.success:
            logging.info("Status RPC call successful")
            if query_result.cloud_stream_running:
                logging.info("AWS Kinesis Stream "+stream_name+" was accepting data.")
            else:
                logging.info("AWS Kinesis Stream "+stream_name+" was not accepting data.")
            
            if query_result.pipeline_running:
                logging.info("The GST Pipeline for RTSP URL "+rtsp_url+" is running.")
            else:
                logging.info("The GST Pipeline for RTSP URL "+rtsp_url+" is not running.")
        else:
            logging.error("Error in checking VOD status")
            logging.error(query_result.status_message)


if __name__ == '__main__':
    main()