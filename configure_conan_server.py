
# This script configures the conan-server file: 'server.conf'
#   It's default location should be: '/root/.conan_server/server.conf'

import os
import sys
import configparser


conan_server_config_file = os.environ.get("CONAN_SERVER_CONFIG_FILE", None)
conan_server_creds_list = os.environ.get("CONAN_SERVER_CREDS_LIST", None)
conan_server_read_permissions = os.environ.get("CONAN_SERVER_READ_PERMISSIONS", None)
conan_server_write_permissions = os.environ.get("CONAN_SERVER_WRITE_PERMISSIONS", None)


def check_params():
	global conan_server_creds_list
	# Check conan-server config file var not null
	if not conan_server_config_file:
		print(f"Error - Var 'conan_server_config_file' is None. \nThe path to conan-server config ini file is null: '{conan_server_config_file}'\nDid you set env var: 'CONAN_SERVER_CONFIG_FILE' to it?\n cannot configure conan-server")
		sys.exit(1)

	# Check conan-server config file exists
	print(f"Checking config file exists")
	if not os.path.exists(conan_server_config_file):
		print(f"Error - Missing conan-server config ini file: '{conan_server_config_file}' \n cannot configure conan-server")
		sys.exit(1)

	# Convert conan_server_creds_list to a list using split(";")
	if conan_server_creds_list:
		print("Preparing creds list to configure")
		conan_server_creds_list = conan_server_creds_list.split(";")
		if type(conan_server_creds_list) != list:
			print(f"Error - Failed to convert var 'conan_server_creds_list={conan_server_creds_list}' to type 'list' using split:  conan_server_creds_list=conan_server_creds_list.split(';')\ntype(conan_server_creds_list)=={type(conan_server_creds_list)}")
			sys.exit(1)


# Read conan-server config file
def read_conf_file():
	try:
		config = configparser.ConfigParser()
		print(f"Reading config file")
		config.read(conan_server_config_file)
		return config
	except BaseException as error_msg:
		print(f"Error - Failed reading conan-server config ini file: '{conan_server_config_file}'\n{error_msg}")
		sys.exit(1)


def validate_config():
	print("Vlidating config file")


def main():
	print(f"Configuring conan-server config ini file: '{conan_server_config_file}' ")
	check_params()
	read_conf_file()
	validate_config()
	print(f"Finished configuring conan-server config ini file: '{conan_server_config_file}' ")


# Start
if __name__ == "__main__":
	main()