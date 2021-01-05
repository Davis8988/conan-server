#!/bin/sh

echo python Version:
python --version
echo Configuring conan-server ini file: '/root/.conan_server/server.conf'
echo Executing: python $(pwd)/configure_conan_server.py
python $(pwd)/configure_conan_server.py


echo Finished configuring conan-server ini file: '/root/.conan_server/server.conf'
echo Starting conan-server:
echo Executing: gunicorn -b 0.0.0.0:9300 -w 4 -t 300 conans.server.server_launcher:app

# Run server on port 9300 with 4 workers and a timeout of 5 minutes (300 seconds)
gunicorn -b 0.0.0.0:9300 -w 4 -t 300 conans.server.server_launcher:app

echo Finished executing conan-server

