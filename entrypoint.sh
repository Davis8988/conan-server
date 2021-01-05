#!/bin/sh

# Set Vars
CONAN_SERVER_LISTEN_IP=${CONAN_SERVER_LISTEN_IP:-0.0.0.0}
CONAN_SERVER_LISTEN_PORT=${CONAN_SERVER_LISTEN_PORT:-9300}
CONAN_SERVER_WORKERS_COUNT=${CONAN_SERVER_WORKERS_COUNT:-4}
CONAN_SERVER_TIMEOUT_SECONDS=${CONAN_SERVER_TIMEOUT_SECONDS:-5}
CONAN_SERVER_USER_NAME=${CONAN_SERVER_USER_NAME:-admin}
CONAN_SERVER_USER_PASSWORD=${CONAN_SERVER_USER_PASSWORD:-12345678}


echo python Version:
python --version

# Configure conan-server ini file
echo Configuring conan-server ini file: '/root/.conan_server/server.conf'
echo Executing: python $(pwd)/configure_conan_server.py
python $(pwd)/configure_conan_server.py
if [ "$?" != "0" ]; then echo Error - Failed configuring conan-server ini file: '/root/.conan_server/server.conf'; echo Failed during execution of: python $(pwd)/configure_conan_server.py; exit 1; fi
echo Finished configuring conan-server ini file: '/root/.conan_server/server.conf'
echo ""

# Start conan-server
echo Conan-Server Vars:
echo   Listen Address: $CONAN_SERVER_LISTEN_IP:$CONAN_SERVER_LISTEN_PORT
echo   Workers: $CONAN_SERVER_WORKERS_COUNT
echo   Timeout Seconds: $CONAN_SERVER_TIMEOUT_SECONDS
echo   User: $CONAN_SERVER_USER_NAME
echo ""

echo Starting conan-server:
echo Executing: gunicorn -b ${CONAN_SERVER_LISTEN_IP}:${CONAN_SERVER_LISTEN_PORT} -w ${CONAN_SERVER_WORKERS_COUNT} -t ${CONAN_SERVER_TIMEOUT_SECONDS} conans.server.server_launcher:app
# Run server on port ${CONAN_SERVER_LISTEN_PORT} with ${CONAN_SERVER_WORKERS_COUNT} workers and a timeout of ${CONAN_SERVER_TIMEOUT_SECONDS} seconds
gunicorn -b ${CONAN_SERVER_LISTEN_IP}:${CONAN_SERVER_LISTEN_PORT} -w ${CONAN_SERVER_WORKERS_COUNT} -t ${CONAN_SERVER_TIMEOUT_SECONDS} conans.server.server_launcher:app

echo Finished executing conan-server

