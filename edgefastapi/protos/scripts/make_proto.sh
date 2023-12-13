#!/bin/bash

#============================================================================
# Name        : make_proto.sh
# Description : Script to auto-generate gRPC libs from proto files
#============================================================================

# path initialization
SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_PATH="$(dirname "$SCRIPTS_PATH")"
cd ${PROJ_PATH}

# pre-process the proto file
cpp -P ${PROJ_PATH}/protos/camera_api_base.proto > \
                                    ${PROJ_PATH}/protos/camera_api.proto
cpp -P ${PROJ_PATH}/protos/vod_api_base.proto > \
                                    ${PROJ_PATH}/protos/vod_api.proto
cpp -P ${PROJ_PATH}/protos/videosave_api_base.proto > \
                                    ${PROJ_PATH}/protos/videosave_api.proto
cpp -P ${PROJ_PATH}/protos/edgeadmin_api_base.proto > \
                                    ${PROJ_PATH}/protos/edgeadmin_api.proto
cpp -P ${PROJ_PATH}/protos/inference_api_base.proto > \
                                    ${PROJ_PATH}/protos/inference_api.proto

# generate python language executables
python3.9 -m grpc_tools.protoc \
            -I ${PROJ_PATH}/protos \
            --python_out=${PROJ_PATH}/python_grpc \
            --grpc_python_out=${PROJ_PATH}/python_grpc camera_api.proto
python3.9 -m grpc_tools.protoc \
            -I ${PROJ_PATH}/protos \
            --python_out=${PROJ_PATH}/python_grpc \
            --grpc_python_out=${PROJ_PATH}/python_grpc vod_api.proto 
python3.9 -m grpc_tools.protoc \
            -I ${PROJ_PATH}/protos \
            --python_out=${PROJ_PATH}/python_grpc \
            --grpc_python_out=${PROJ_PATH}/python_grpc videosave_api.proto
python3.9 -m grpc_tools.protoc \
            -I ${PROJ_PATH}/protos \
            --python_out=${PROJ_PATH}/python_grpc \
            --grpc_python_out=${PROJ_PATH}/python_grpc edgeadmin_api.proto 
python3.9 -m grpc_tools.protoc \
            -I ${PROJ_PATH}/protos \
            --python_out=${PROJ_PATH}/python_grpc \
            --grpc_python_out=${PROJ_PATH}/python_grpc inference_api.proto 

# cleanup
rm ${PROJ_PATH}/protos/camera_api.proto
rm ${PROJ_PATH}/protos/vod_api.proto
rm ${PROJ_PATH}/protos/videosave_api.proto
rm ${PROJ_PATH}/protos/edgeadmin_api.proto
rm ${PROJ_PATH}/protos/inference_api.proto
