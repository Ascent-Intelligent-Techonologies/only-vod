# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import videosave_api_pb2 as videosave__api__pb2


class VideoSaveServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HealthCheck = channel.unary_unary(
                '/VideoSaveService.VideoSaveService/HealthCheck',
                request_serializer=videosave__api__pb2.HealthCheckMessage.SerializeToString,
                response_deserializer=videosave__api__pb2.HealthCheckResult.FromString,
                )
        self.VideoSave = channel.unary_unary(
                '/VideoSaveService.VideoSaveService/VideoSave',
                request_serializer=videosave__api__pb2.VideoSaveMessage.SerializeToString,
                response_deserializer=videosave__api__pb2.VideoSaveResult.FromString,
                )
        self.StopVideoSave = channel.unary_unary(
                '/VideoSaveService.VideoSaveService/StopVideoSave',
                request_serializer=videosave__api__pb2.VideoSaveMessage.SerializeToString,
                response_deserializer=videosave__api__pb2.VideoSaveResult.FromString,
                )
        self.GetFrame = channel.unary_unary(
                '/VideoSaveService.VideoSaveService/GetFrame',
                request_serializer=videosave__api__pb2.GetFrameMessage.SerializeToString,
                response_deserializer=videosave__api__pb2.S3PathMessage.FromString,
                )
        self.GetAlert = channel.unary_unary(
                '/VideoSaveService.VideoSaveService/GetAlert',
                request_serializer=videosave__api__pb2.GetAlertMessage.SerializeToString,
                response_deserializer=videosave__api__pb2.GetAlertResponse.FromString,
                )


class VideoSaveServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def HealthCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VideoSave(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopVideoSave(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFrame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAlert(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VideoSaveServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=videosave__api__pb2.HealthCheckMessage.FromString,
                    response_serializer=videosave__api__pb2.HealthCheckResult.SerializeToString,
            ),
            'VideoSave': grpc.unary_unary_rpc_method_handler(
                    servicer.VideoSave,
                    request_deserializer=videosave__api__pb2.VideoSaveMessage.FromString,
                    response_serializer=videosave__api__pb2.VideoSaveResult.SerializeToString,
            ),
            'StopVideoSave': grpc.unary_unary_rpc_method_handler(
                    servicer.StopVideoSave,
                    request_deserializer=videosave__api__pb2.VideoSaveMessage.FromString,
                    response_serializer=videosave__api__pb2.VideoSaveResult.SerializeToString,
            ),
            'GetFrame': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFrame,
                    request_deserializer=videosave__api__pb2.GetFrameMessage.FromString,
                    response_serializer=videosave__api__pb2.S3PathMessage.SerializeToString,
            ),
            'GetAlert': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAlert,
                    request_deserializer=videosave__api__pb2.GetAlertMessage.FromString,
                    response_serializer=videosave__api__pb2.GetAlertResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'VideoSaveService.VideoSaveService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VideoSaveService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def HealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/VideoSaveService.VideoSaveService/HealthCheck',
            videosave__api__pb2.HealthCheckMessage.SerializeToString,
            videosave__api__pb2.HealthCheckResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VideoSave(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/VideoSaveService.VideoSaveService/VideoSave',
            videosave__api__pb2.VideoSaveMessage.SerializeToString,
            videosave__api__pb2.VideoSaveResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopVideoSave(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/VideoSaveService.VideoSaveService/StopVideoSave',
            videosave__api__pb2.VideoSaveMessage.SerializeToString,
            videosave__api__pb2.VideoSaveResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFrame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/VideoSaveService.VideoSaveService/GetFrame',
            videosave__api__pb2.GetFrameMessage.SerializeToString,
            videosave__api__pb2.S3PathMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAlert(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/VideoSaveService.VideoSaveService/GetAlert',
            videosave__api__pb2.GetAlertMessage.SerializeToString,
            videosave__api__pb2.GetAlertResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)