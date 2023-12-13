"""
============================================================================
# Name        : edgeadmin_server.py
# Description : gRPC server for the Edge Admin service 
============================================================================
"""

# import modules
import os
import sys
import signal
import logging
import threading
from pathlib import Path
from concurrent import futures
from datetime import datetime,timedelta
import subprocess
import cv2
import requests

# add import path
python_grpc_path = Path(__file__).resolve().parents[1] / 'protos/python_grpc'
sys.path.insert(1, str(python_grpc_path))

# import grpc dependencies
import grpc
import edgeadmin_api_pb2_grpc
from edgeadmin_api_pb2 import RTSPHealthCheckResult, RTSPFeedHealthCheck, ListRtspUrl, RtspUrlMessage

# load env variables
server_port = str(os.environ['SERVER_PORT'])
server_address = str(os.environ['SERVER_ADDRESS'])
SQL_BASE_URL = str(os.environ['SQL_BASE_URL'])


class EdgeAdminServiceImpl(edgeadmin_api_pb2_grpc.EdgeAdminServiceServicer):
    """
    EdgeAdminServiceImpl class for gRPC EdgeAdmin service
    """
    def __init__(self):
        """
        Class initialiser for EdgeAdminServiceImpl
        """
        logging.info('Initializing EdgeAdmin Service')

    def error_handling(self, request_status, console_log, request_type, context):
        """
        Error handling function
        :param request_status: Flag to indicate status of rpc call
        :param console_log: Console log string to be published to logger
        :param request_type: Type of rpc being called for logging purposes
        :param context: Context variable of gRPC service to return as response
        """
        if request_status:
            logging.info(console_log)
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error processing request')
            logging.error('Internal error processing ' + request_type)
            logging.error(console_log)


    def RTSPHealthCheck(self, request, context):
        """
        gRPC rpc function to check status of multiple RTSP feeds
        :param request: Input request to get health check status
        :param context: Context argument to log status of request
        """
        # initialize reponse message
        request_status = True
        response = RTSPHealthCheckResult()
        console_log = 'Sending health check'
        # process the request content
        try:
            logging.info("Health Check for RTSP feeds started")
            
            for rtsp_url_message in request.rtsp_urls:
                
                rtsp_feed_health = RTSPFeedHealthCheck()
                rtsp_url = rtsp_url_message.rtsp_url
                
                logging.info("Checking health for URL: "+rtsp_url)
                
                cap = cv2.VideoCapture(rtsp_url)
                
                if cap.isOpened(): #Checking if camera is working for individual RTSP feed
                    rtsp_feed_health.status_flag = True
                    rtsp_feed_health.status_message = "The RTSP feed at URL "+rtsp_url+" is running"
                
                else:
                    rtsp_feed_health.status_flag = False
                    rtsp_feed_health.status_message = "The RTSP feed at URL "+rtsp_url+" is not running"
                
                response.feeds.append(rtsp_feed_health)
            
            logging.info("Health Check complete")
            response.success = True
            response.status_message = "Health Check successful"

        except Exception as error_msg:
            # error handling for processing request
            request_status = False
            console_log = str(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error processing request: ' + str(error_msg))
            response.success = False
            response.status_message = console_log
            self.error_handling(request_status, console_log, 'Health Check', context)
        
        return response

    def GetRtspUrl (self, request, context):
        """gRPC rpc function to get rtsp url's from sql
        Args:
            request (_type_): _description_
            context (_type_): _description_
        """
        request_status = True
        response = ListRtspUrl()
        console_log = 'getting rtsp urls'
        device_id = request.device_id
        try:
            # logging.info("Getting RTSP urls started")
            resp = requests.get(f"{SQL_BASE_URL}options?device_id={device_id}")
            if resp.status_code ==200:
                list_cameras = resp.json()
                # logging.info(list_cameras)
                for cam in list_cameras:
                    rtsp_url_message = RtspUrlMessage()
                    rtsp_url_message.rtsp_url = cam["rtsp"]
                    response.rtsp_urls.append(rtsp_url_message)
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details('Error processing request: ' + str(resp.content))
                self.error_handling(False, str(resp.content), 'Get rtsp url', context)
        except Exception as error_msg:
            # error handling for processing request
            request_status = False
            console_log = str(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error processing request: ' + str(error_msg))
            response.success = False
            response.status_message = console_log
            self.error_handling(request_status, console_log, 'Health Check', context)
        
        return response
            
        
        
# helper function for terminating the server
terminate = threading.Event()
def terminate_server(signum, frame):
    """
    Utility to add terminate signal to thread pool
    :param signum: Signal number
    :param frame: Frame argument
    """
    logging.info('Got signal {}, {}'.format(signum, frame))
    terminate.set()


def main():
    """
    Main function to initiate EdgeAdmin server
    """
    # setup signal handling and logging
    signal.signal(signal.SIGINT, terminate_server)
    logging.basicConfig(level=logging.DEBUG)

    # setup the server address
    server_url = server_address + ':' + str(server_port)

    # instantiate the service implementation
    service = EdgeAdminServiceImpl()

    # create the grpc server handling 2 concurrent requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

    # add an backend servicer to gRPC server
    edgeadmin_api_pb2_grpc.add_EdgeAdminServiceServicer_to_server(service, server)

    # assign a port to the server
    server.add_insecure_port(server_url)

    # start the server
    server.start()
    logging.info('EdgeAdminService server listening on port ' + server_port)

    terminate.wait()
    logging.info('Stopping the server...')

    server.stop(1).wait()
    logging.info('EdgeAdminService server was stopped')


if __name__ == '__main__':
    main()