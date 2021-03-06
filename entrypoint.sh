#!/bin/sh

# Set Vars/Default Values
export CONAN_SERVER_LISTEN_IP=${CONAN_SERVER_LISTEN_IP:-0.0.0.0}
export CONAN_SERVER_LISTEN_PORT=${CONAN_SERVER_LISTEN_PORT:-9300}
export CONAN_SERVER_WORKERS_COUNT=${CONAN_SERVER_WORKERS_COUNT:-4}
export CONAN_SERVER_TIMEOUT_SECONDS=${CONAN_SERVER_TIMEOUT_SECONDS:-5}
export CONAN_SERVER_CONFIG_FILE=${CONAN_SERVER_CONFIG_FILE:-/root/.conan_server/server.conf}

echo ""

# Print Python version
echo python Version: $(python --version)

# Check script exists:
if [ ! -f "$(pwd)/configure_conan_server.py" ]; then echo "Error - Missing or unreachable python script to configure conan-server config file: $(pwd)/configure_conan_server.py"; echo "Aborting.." ; exit 1; fi

# Configure conan-server ini file
echo "Configuring conan-server ini file: '$CONAN_SERVER_CONFIG_FILE'"
echo Executing: python $(pwd)/configure_conan_server.py
python $(pwd)/configure_conan_server.py
if [ "$?" != "0" ]; then echo "Error - Failed configuring conan-server ini file: '$CONAN_SERVER_CONFIG_FILE'"; echo "Failed during execution of: python $(pwd)/configure_conan_server.py" ; exit 1; fi
echo "Finished configuring conan-server ini file: '$CONAN_SERVER_CONFIG_FILE'"
echo ""

# Print Confs
echo Conan-Server Vars:
echo "  Config File: '$CONAN_SERVER_CONFIG_FILE'"
echo "  Listen Address: '$CONAN_SERVER_LISTEN_IP:$CONAN_SERVER_LISTEN_PORT'"
echo "  Workers: '$CONAN_SERVER_WORKERS_COUNT'"
echo "  Timeout Seconds: '$CONAN_SERVER_TIMEOUT_SECONDS'"
echo "  Write Permissions: '$CONAN_SERVER_WRITE_PERMISSIONS_LIST'"
echo "  Read Permissions: '$CONAN_SERVER_READ_PERMISSIONS_LIST'"
echo ""

# Start conan-server
echo "Starting conan-server:"
echo "Executing: gunicorn -b ${CONAN_SERVER_LISTEN_IP}:${CONAN_SERVER_LISTEN_PORT} -w ${CONAN_SERVER_WORKERS_COUNT} -t ${CONAN_SERVER_TIMEOUT_SECONDS} conans.server.server_launcher:app"
# Run server on port ${CONAN_SERVER_LISTEN_PORT} with ${CONAN_SERVER_WORKERS_COUNT} workers and a timeout of ${CONAN_SERVER_TIMEOUT_SECONDS} seconds
gunicorn -b ${CONAN_SERVER_LISTEN_IP}:${CONAN_SERVER_LISTEN_PORT} -w ${CONAN_SERVER_WORKERS_COUNT} -t ${CONAN_SERVER_TIMEOUT_SECONDS} conans.server.server_launcher:app

echo "Finished executing conan-server"

