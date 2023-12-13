# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import edgeadmin_api_pb2 as edgeadmin__api__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class EdgeAdminServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RTSPHealthCheck = channel.unary_unary(
                '/EdgeAdminService.EdgeAdminService/RTSPHealthCheck',
                request_serializer=edgeadmin__api__pb2.ListRtspUrl.SerializeToString,
                response_deserializer=edgeadmin__api__pb2.RTSPHealthCheckResult.FromString,
                )
        self.GetRtspUrl = channel.unary_unary(
                '/EdgeAdminService.EdgeAdminService/GetRtspUrl',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=edgeadmin__api__pb2.ListRtspUrl.FromString,
                )


class EdgeAdminServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RTSPHealthCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRtspUrl(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EdgeAdminServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RTSPHealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.RTSPHealthCheck,
                    request_deserializer=edgeadmin__api__pb2.ListRtspUrl.FromString,
                    response_serializer=edgeadmin__api__pb2.RTSPHealthCheckResult.SerializeToString,
            ),
            'GetRtspUrl': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRtspUrl,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=edgeadmin__api__pb2.ListRtspUrl.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'EdgeAdminService.EdgeAdminService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EdgeAdminService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RTSPHealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/EdgeAdminService.EdgeAdminService/RTSPHealthCheck',
            edgeadmin__api__pb2.ListRtspUrl.SerializeToString,
            edgeadmin__api__pb2.RTSPHealthCheckResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRtspUrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/EdgeAdminService.EdgeAdminService/GetRtspUrl',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            edgeadmin__api__pb2.ListRtspUrl.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
