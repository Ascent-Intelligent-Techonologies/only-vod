"""
============================================================================
# Name        : edgeadmin_client.py
# Description : 
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
import edgeadmin_api_pb2_grpc
from edgeadmin_api_pb2 import  *

# load env variables
server_port = str(os.environ['SERVER_PORT'])
server_address = str(os.environ['SERVER_ADDRESS'])

empty = google_dot_protobuf_dot_empty__pb2.Empty()
#   response = stub.NodeConfig(empty)

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
                time.sleep(5)
                self.is_grpc_active = True
            return True
        except Exception as error:
            logging.error(error)
            self.is_grpc_active = False
            return False


    def health_check(self,rtsp_urls):
        """
        Utility function to call terminate camera rpc
        :param config: Config dictionary with request details
        """
        if self.is_grpc_active:
            # initialize request message
            request = ListRtspUrl()

            for rtsp_url in rtsp_urls:
                rtsp_url_message = RtspUrlMessage()
                rtsp_url_message.rtsp_url = rtsp_url
                request.rtsp_urls.append(rtsp_url_message)

            # call the rpc
            result = self.stub.RTSPHealthCheck(request)

            return True, result
        else:
            return False, 'gRPC channel is inactive'
    
    def get_rtsp_url(self):
        if self.is_grpc_active:
            result = self.stub.GetRtspUrl(empty)
            return True, result


def main():
    """
    Main function for edgeadmin service client
    """
    parser = argparse.ArgumentParser(
        description='Client for edgeadmin service')
    parser.add_argument(
        '-a', '--action', type=str,
        required= True,
        help='Action to use for edgeadmin client',
        choices=["healthcheck","get_rtsp_url"])
    parser.add_argument(
        '--urls', type=str,
        default="rtsp://192.168.151.50:8554/mystream",
        help="Comma separated list of RTSP urls.\nFor eg. rtsp://192.168.151.50:8554/mystream1,rtsp://192.168.151.50:8554/mystream2,rtsp://192.168.151.50:8554/mystream3"
    )

    args = parser.parse_args()

    # setup logging
    logging.basicConfig(level=logging.DEBUG)
    
    # initialize the edgeadmin service node
    edgeadmin_client = EdgeAdminServiceNode()

    # activate the grpc channel
    res = edgeadmin_client.activate_grpc_channel()

    if not res:
        logging.error('Error with gRPC server connection')
        return -1
    
    if args.action == "healthcheck":

        rtsp_urls = [url.strip() for url in args.urls.split(",")]

        query_success, query_result = edgeadmin_client.health_check(rtsp_urls)
        if query_success and query_result.success:
            logging.info("Health Check RPC call successful")
            for feed_health in query_result.feeds:
                logging.info(feed_health.status_message)
        else:
            logging.error("Error in health check RPC call")
            logging.error(query_result.status_message)
    elif args.action == "get_rtsp_url" :
        query_success, query_result = edgeadmin_client.get_rtsp_url()
        logging.info(query_result)
    

if __name__ == '__main__':
    main()