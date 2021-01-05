
# This script configures the conan-server file: 'server.conf'
#   It's default location should be: '/root/.conan_server/server.conf'

import os
import sys
import configparser


conan_server_config_file = os.environ.get("CONAN_SERVER_CONFIG_FILE", None)
conan_server_user_name = os.environ.get("CONAN_SERVER_USER_NAME", None)
conan_server_user_pass = os.environ.get("CONAN_SERVER_USER_PASS", None)
conan_server_read_permissions = os.environ.get("CONAN_SERVER_READ_PERMISSIONS", None)


# Check conan-server config file exists
print(f"Configuring conan-server config ini file: '{conan_server_config_file}' ")
if not os.path.exists(conan_server_config_file):
	print(f"Error - Missing conan-server config ini file: '{conan_server_config_file}' \n cannot configure conan-server")
	sys.exit(1)
	

# Read conan-server config file
try:
	config = configparser.ConfigParser()
	print(f"Reading config ini file: '{conan_server_config_file}' ")
	config.read(conan_server_config_file)
except BaseException as error_msg:
	print(f"Error - Failed reading conan-server config ini file: '{conan_server_config_file}'\n{error_msg}")
	sys.exit(1)
