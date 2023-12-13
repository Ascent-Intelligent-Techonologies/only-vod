"""
============================================================================
# Name        : vod_server.py
# Description : gRPC server for the VOD service 
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
import boto3
import cv2
import psutil


# add import path
python_grpc_path = Path(__file__).resolve().parents[1] / 'protos/python_grpc'
sys.path.insert(1, str(python_grpc_path))

# import grpc dependencies
import grpc
import vod_api_pb2_grpc
from vod_api_pb2 import VODStartResponse, VODStatusResponse, VODStopResponse, HealthCheckResult, RTSPFeedHealthCheck

# load env variables
server_port = str(os.environ['SERVER_PORT'])
server_address = str(os.environ['SERVER_ADDRESS'])
ACCESSKEY = str(os.environ['ACCESSKEY'])
SECRETKEY = str(os.environ['SECRETKEY'])


# Cloudwatch object for monitoring stream status
cloudwatch = boto3.client('cloudwatch',
                            region_name="ap-south-1",
                            aws_access_key_id=ACCESSKEY,
                            aws_secret_access_key= SECRETKEY)



class VODServiceImpl(vod_api_pb2_grpc.VODServiceServicer):
    """
    VODServiceImpl class for gRPC VOD service
    """
    def __init__(self):
        """
        Class initialiser for VODServiceImpl
        """
        logging.info('Initializing VOD Service')
        # Create a dictionary to map RTSP URLs to pids of the process streaming from that URL
        self.current_streams = {}

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

    def IsStreamRunning(self,rtsp_url):
        """
        Helper function for checking if a stream is running
        by checking the process pid
        :param rtsp_url: RTSP URL of the stream (string)
        """
        if rtsp_url in self.current_streams:
            gst_pid = self.current_streams[rtsp_url]
            pipeline_is_running =  psutil.pid_exists(gst_pid)
            if pipeline_is_running:
                return True
            else:
                del self.current_streams[rtsp_url]
                return False
        else:
            return False


    def CheckVODStatus(self,request,context):
        """
        gRPC rpc function to check cloudwatch metrics for a stream
        and the status of the background gst pipeline
        Note: The cloudwatch metrics are delayed by a few minutes 
        and should not be used for real-time debugging.  
        :param request: Input request to get VOD check parameters
        :param context: Context argument to log status of request
        """
        # initialize response message
        response = VODStatusResponse()
        request_status = True
        console_log = None
        
        # process the request content
        try:
            stream_name = request.stream_name
            metric_name = "PutMedia.IncomingBytes"

            end_time = datetime.now()
            start_time = end_time - timedelta(seconds=60) #Get logs for duration of 1 min
            end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            period = 60 #return logs every minute

            cloud_logs = cloudwatch.get_metric_data(
                    MetricDataQueries=[
                        {
                            'Id': 'stream_running',
                            'MetricStat': {
                                'Metric': {
                                    'Namespace': 'AWS/KinesisVideo',
                                    'MetricName': metric_name,
                                    'Dimensions': [
                                        {
                                            'Name': 'StreamName',
                                            'Value': stream_name
                                        },
                                    ]
                                },
                                'Period':period,
                                'Stat':'Sum'
                            },
                            'ReturnData': True
                        },
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    ScanBy='TimestampAscending',
                )
            
            if cloud_logs["MetricDataResults"][0]["Values"]:
                response.cloud_stream_running = True
            else:
                response.cloud_stream_running = False
            

            response.cloudwatch_logs = str(cloud_logs)

            rtsp_url = request.rtsp_url
            if self.IsStreamRunning(rtsp_url):
                response.pipeline_running = True
            else:
                response.pipeline_running = False

            response.success = True
            response.status_message = "VOD status check successful"

        except Exception as error_msg:
            # error handling for processing request
            request_status = False
            console_log = str(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error processing request: ' + str(error_msg))
            response.success = False
            response.status_message = console_log            
            self.error_handling(request_status, console_log, 'Check VOD Status', context)

        return response
        

    def StartVOD(self, request, context):
        """
        gRPC rpc function to start VOD streaming
        :param request: Input request to get stream parameters
        :param context: Context argument to log status of request
        """
        # initialize response message
        response = VODStartResponse()
        request_status = True
        console_log = 'Starting VOD'
        
        # process the request content
        try:
            stream_name = request.stream_name
            rtsp_url = request.rtsp_url

            if self.IsStreamRunning(rtsp_url):
                response.success = True
                response.status_message = "Stream already running for RTSP URL: "+rtsp_url
                return response

            cmd = f"""gst-launch-1.0 -v rtspsrc location={rtsp_url} short-header=TRUE ! rtph264depay ! h264parse ! kvssink stream-name={stream_name} storage-size=128 access-key=$ACCESSKEY secret-key=$SECRETKEY aws-region=$AWSREGION"""
            p = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT) 
            # The above command opens a new shell and starts the gst pipeline in this shell
            
            gst_pid = int(p.pid)+1 # +1 because p.pid is the subprocess shell which starts the pipeline 
            self.current_streams[rtsp_url] = gst_pid
            logging.info("gst pipeline started to run stream at:"+stream_name)
            
            response.success = True
            response.status_message = "Request sent to start VOD on stream:"+stream_name

        except Exception as error_msg:
            # error handling for processing request
            request_status = False
            console_log = str(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error processing request: ' + str(error_msg))
            response.success = False
            response.status_message = console_log
            self.error_handling(request_status, console_log, 'Start VOD', context)

        return response

    def StopVOD(self, request, context):
        """
        gRPC rpc function to stop VOD streaming
        :param request: Input request to get rtsp url
        :param context: Context argument to log status of request
        """
        # initialize response message
        response = VODStopResponse()
        request_status = True
        console_log = 'Starting VOD'
        
        # process the request content
        try:
            rtsp_url = request.rtsp_url

            if not self.IsStreamRunning(rtsp_url):
                response.success = True
                response.status_message = "No Stream running for the RTSP URL: "+rtsp_url
                return response


            stream_pid = self.current_streams[rtsp_url] # get pid for gst pipeline running the stream
            shell_pid = stream_pid - 1 # pid of the Popen shell which started the pipeline

            os.kill(stream_pid, signal.SIGTERM) # Killing gst streaming pipeline
            os.kill(shell_pid, signal.SIGTERM) # Killing the shell which is running the pipeline

            del self.current_streams[rtsp_url]

            logging.info("Terminated streaming pipeline from RTSP feed: "+rtsp_url)
            response.success = True
            response.status_message = "Stoppped streaming from RTSP feed: "+rtsp_url

        except Exception as error_msg:
            # error handling for processing request
            request_status = False
            console_log = str(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error processing request: ' + str(error_msg))
            response.success = False
            response.status_message = console_log
            self.error_handling(request_status, console_log, 'Stop VOD', context)

        return response

    def HealthCheck(self, request, context):
        """
        gRPC rpc function to check status of multiple RTSP feeds
        :param request: Input request to get health check status
        :param context: Context argument to log status of request
        """
        # initialize reponse message
        request_status = True
        response = HealthCheckResult()
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
    Main function to initiate vod server
    """
    # setup signal handling and logging
    signal.signal(signal.SIGINT, terminate_server)
    logging.basicConfig(level=logging.DEBUG)

    # setup the server address
    server_url = server_address + ':' + str(server_port)

    # instantiate the service implementation
    service = VODServiceImpl()

    # create the grpc server handling 2 concurrent requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

    # add an backend servicer to gRPC server
    vod_api_pb2_grpc.add_VODServiceServicer_to_server(service, server)

    # assign a port to the server
    server.add_insecure_port(server_url)

    # start the server
    server.start()
    logging.info('VODService server listening on port ' + server_port)

    terminate.wait()
    logging.info('Stopping the server...')

    server.stop(1).wait()
    logging.info('VODService server was stopped')


if __name__ == '__main__':
    main()