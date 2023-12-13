# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: edgeadmin_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='edgeadmin_api.proto',
  package='EdgeAdminService',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13\x65\x64geadmin_api.proto\x12\x10\x45\x64geAdminService\x1a\x1bgoogle/protobuf/empty.proto\"B\n\x0bListRtspUrl\x12\x33\n\trtsp_urls\x18\x01 \x03(\x0b\x32 .EdgeAdminService.RtspUrlMessage\"&\n\x11GetRtspUrlMessage\x12\x11\n\tdevice_id\x18\x01 \x01(\t\"\"\n\x0eRtspUrlMessage\x12\x10\n\x08rtsp_url\x18\x01 \x01(\t\"B\n\x13RTSPFeedHealthCheck\x12\x13\n\x0bstatus_flag\x18\x01 \x01(\x08\x12\x16\n\x0estatus_message\x18\x02 \x01(\t\"v\n\x15RTSPHealthCheckResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x16\n\x0estatus_message\x18\x02 \x01(\t\x12\x34\n\x05\x66\x65\x65\x64s\x18\x03 \x03(\x0b\x32%.EdgeAdminService.RTSPFeedHealthCheck2\xc3\x01\n\x10\x45\x64geAdminService\x12[\n\x0fRTSPHealthCheck\x12\x1d.EdgeAdminService.ListRtspUrl\x1a\'.EdgeAdminService.RTSPHealthCheckResult\"\x00\x12R\n\nGetRtspUrl\x12#.EdgeAdminService.GetRtspUrlMessage\x1a\x1d.EdgeAdminService.ListRtspUrl\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_LISTRTSPURL = _descriptor.Descriptor(
  name='ListRtspUrl',
  full_name='EdgeAdminService.ListRtspUrl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rtsp_urls', full_name='EdgeAdminService.ListRtspUrl.rtsp_urls', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=136,
)


_GETRTSPURLMESSAGE = _descriptor.Descriptor(
  name='GetRtspUrlMessage',
  full_name='EdgeAdminService.GetRtspUrlMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='EdgeAdminService.GetRtspUrlMessage.device_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=176,
)


_RTSPURLMESSAGE = _descriptor.Descriptor(
  name='RtspUrlMessage',
  full_name='EdgeAdminService.RtspUrlMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rtsp_url', full_name='EdgeAdminService.RtspUrlMessage.rtsp_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=212,
)


_RTSPFEEDHEALTHCHECK = _descriptor.Descriptor(
  name='RTSPFeedHealthCheck',
  full_name='EdgeAdminService.RTSPFeedHealthCheck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status_flag', full_name='EdgeAdminService.RTSPFeedHealthCheck.status_flag', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status_message', full_name='EdgeAdminService.RTSPFeedHealthCheck.status_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=214,
  serialized_end=280,
)


_RTSPHEALTHCHECKRESULT = _descriptor.Descriptor(
  name='RTSPHealthCheckResult',
  full_name='EdgeAdminService.RTSPHealthCheckResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='EdgeAdminService.RTSPHealthCheckResult.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status_message', full_name='EdgeAdminService.RTSPHealthCheckResult.status_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feeds', full_name='EdgeAdminService.RTSPHealthCheckResult.feeds', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=282,
  serialized_end=400,
)

_LISTRTSPURL.fields_by_name['rtsp_urls'].message_type = _RTSPURLMESSAGE
_RTSPHEALTHCHECKRESULT.fields_by_name['feeds'].message_type = _RTSPFEEDHEALTHCHECK
DESCRIPTOR.message_types_by_name['ListRtspUrl'] = _LISTRTSPURL
DESCRIPTOR.message_types_by_name['GetRtspUrlMessage'] = _GETRTSPURLMESSAGE
DESCRIPTOR.message_types_by_name['RtspUrlMessage'] = _RTSPURLMESSAGE
DESCRIPTOR.message_types_by_name['RTSPFeedHealthCheck'] = _RTSPFEEDHEALTHCHECK
DESCRIPTOR.message_types_by_name['RTSPHealthCheckResult'] = _RTSPHEALTHCHECKRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListRtspUrl = _reflection.GeneratedProtocolMessageType('ListRtspUrl', (_message.Message,), {
  'DESCRIPTOR' : _LISTRTSPURL,
  '__module__' : 'edgeadmin_api_pb2'
  # @@protoc_insertion_point(class_scope:EdgeAdminService.ListRtspUrl)
  })
_sym_db.RegisterMessage(ListRtspUrl)

GetRtspUrlMessage = _reflection.GeneratedProtocolMessageType('GetRtspUrlMessage', (_message.Message,), {
  'DESCRIPTOR' : _GETRTSPURLMESSAGE,
  '__module__' : 'edgeadmin_api_pb2'
  # @@protoc_insertion_point(class_scope:EdgeAdminService.GetRtspUrlMessage)
  })
_sym_db.RegisterMessage(GetRtspUrlMessage)

RtspUrlMessage = _reflection.GeneratedProtocolMessageType('RtspUrlMessage', (_message.Message,), {
  'DESCRIPTOR' : _RTSPURLMESSAGE,
  '__module__' : 'edgeadmin_api_pb2'
  # @@protoc_insertion_point(class_scope:EdgeAdminService.RtspUrlMessage)
  })
_sym_db.RegisterMessage(RtspUrlMessage)

RTSPFeedHealthCheck = _reflection.GeneratedProtocolMessageType('RTSPFeedHealthCheck', (_message.Message,), {
  'DESCRIPTOR' : _RTSPFEEDHEALTHCHECK,
  '__module__' : 'edgeadmin_api_pb2'
  # @@protoc_insertion_point(class_scope:EdgeAdminService.RTSPFeedHealthCheck)
  })
_sym_db.RegisterMessage(RTSPFeedHealthCheck)

RTSPHealthCheckResult = _reflection.GeneratedProtocolMessageType('RTSPHealthCheckResult', (_message.Message,), {
  'DESCRIPTOR' : _RTSPHEALTHCHECKRESULT,
  '__module__' : 'edgeadmin_api_pb2'
  # @@protoc_insertion_point(class_scope:EdgeAdminService.RTSPHealthCheckResult)
  })
_sym_db.RegisterMessage(RTSPHealthCheckResult)



_EDGEADMINSERVICE = _descriptor.ServiceDescriptor(
  name='EdgeAdminService',
  full_name='EdgeAdminService.EdgeAdminService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=403,
  serialized_end=598,
  methods=[
  _descriptor.MethodDescriptor(
    name='RTSPHealthCheck',
    full_name='EdgeAdminService.EdgeAdminService.RTSPHealthCheck',
    index=0,
    containing_service=None,
    input_type=_LISTRTSPURL,
    output_type=_RTSPHEALTHCHECKRESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetRtspUrl',
    full_name='EdgeAdminService.EdgeAdminService.GetRtspUrl',
    index=1,
    containing_service=None,
    input_type=_GETRTSPURLMESSAGE,
    output_type=_LISTRTSPURL,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EDGEADMINSERVICE)

DESCRIPTOR.services_by_name['EdgeAdminService'] = _EDGEADMINSERVICE

# @@protoc_insertion_point(module_scope)