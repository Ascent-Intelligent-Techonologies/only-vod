import logging
import boto3
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

kinesis_client = boto3.client("kinesisvideo", region_name=os.environ["AWSREGION"]
                              ,aws_access_key_id=os.environ["ACCESSKEY"]
                              ,aws_secret_access_key=os.environ["SECRETKEY"])


class KinesisHelper:
    """Encapsulates a Kinesis stream."""
    def __init__(self, kinesis_client):
        """
        :param kinesis_client: A Boto3 Kinesis client.
        """
        self.kinesis_client = kinesis_client

    def create(self, name ):
        """
        Creates a stream.
        :param name: The name of the stream.
        """
        resp = self.kinesis_client.create_stream(StreamName=name,DataRetentionInHours=1)
        return resp

    def list_streams(self):
        """
        Lists all streams.
        :return: A list of stream names and stream arn.
        """
        
        response = self.kinesis_client.list_streams()
        streams = []
        for stream in response['StreamInfoList']:                
            streams.append({'StreamName':stream['StreamName'],'StreamARN': stream['StreamARN']})
        return streams
        
        
    def describe(self, name):
        """
        Gets metadata about a stream.
        :param name: The name of the stream.
        :return: Metadata about the stream.
        """
        response = self.kinesis_client.describe_stream(StreamName=name)
        return response
        
        
    def delete(self, name):
        """
        Deletes a stream.
        """
        
        self.kinesis_client.delete_stream(StreamARN= name )
        logger.info(f"Deleted stream {name}")
        
kinesis_helper = KinesisHelper(kinesis_client)