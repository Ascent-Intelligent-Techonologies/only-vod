#!/bin/bash

#============================================================================
# Name        : start_server.sh
# Description : Script to start up camera server in gRPC
#============================================================================

# initialization

SCRIPTS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null 2>&1 && pwd )"
PROJ_PATH="$(dirname "$SCRIPTS_PATH")"
cd ${PROJ_PATH}

shopt -s expand_aliases
source ~/.bash_aliases
# start the camera api server
python src/edgeadmin_server.py
