
# This script configures the conan-server file: 'server.conf'
#   It's default location should be: '/root/.conan_server/server.conf'

import os
import sys
import configparser


conan_server_config_file = os.environ.get("CONAN_SERVER_CONFIG_FILE", None)
conan_server_creds_list = os.environ.get("CONAN_SERVER_CREDS_LIST", None)
conan_server_read_permissions = os.environ.get("CONAN_SERVER_READ_PERMISSIONS", None)
conan_server_write_permissions = os.environ.get("CONAN_SERVER_WRITE_PERMISSIONS", None)

required_sections = ["server", "write_permissions", "read_permissions", "users"]

def get_default_server_settings():
	default_server_section_data = {
		'jwt_secret' : "sJTkzgNOewoPlGMpQYOKWnCd",
		'jwt_expire_minutes' : "120",
		'ssl_enabled' : "False",
		'port' : "9300",
		'public_port' : "",
		'host_name' : "localhost",
		'authorize_timeout' : "1800",
		'disk_storage_path' : "./data",
		'disk_authorize_timeout' : "1800",
		'updown_secret' : "ZlKsEGVuWWlmqWoOIGkVnSRQ"
	}
	default_server_settings_config = configparser.ConfigParser()
	default_server_settings_config.add_section("server")
	for k,v in default_server_section_data.items():
		default_server_settings_config["server"][k] = v
	return default_server_settings_config


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


def validate_config(config, default_server_settings):
	print("Validating config file")
	for sec_name in required_sections:
		if not config.has_section(sec_name):
			print(f"Adding missing section to config file: '{sec_name}'")
			config.add_section(sec_name)
	for k,v in default_server_settings.items():
		if not config.has_option("server", k):
			print(f"Adding missing entry to config file: server.{k} = {v}")
			config["server"][k] = v

	print("Finished validating config file")


def main():
	print(f"Configuring conan-server config ini file: '{conan_server_config_file}' ")
	check_params()
	default_server_settings = get_default_server_settings()
	config = read_conf_file()
	validate_config(config, default_server_settings)
	print(f"Finished configuring conan-server config ini file: '{conan_server_config_file}' ")


# Start
if __name__ == "__main__":
	main()