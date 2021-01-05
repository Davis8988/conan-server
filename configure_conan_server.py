
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


def convert_to_list(string_var, delimiter):
	if not string_var:
		return None
	converted_list = string_var.split(";")
	if type(converted_list) != list:
		print(f"Error - Failed to convert var 'string_var={string_var}' to type 'list' using split(';')")
		return None
	if len(converted_list) == 0:
		return None
	return converted_list


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
	return config


def validate_creds(creds):
	if not creds:
		return False
	if ':' not in creds:
		print(f"Warning - Skipping configure creds of: '{creds}' becuase they are not in the right format\n Should be: 'username: pass'. Example: 'david: 123' ")
		return False
	username, password = creds.split(":")
	if len(username) == 0:
		print(f"Warning - Skipping configure creds of: '{creds}' becuase they are not in the right format\nusername is of length 0\nShould be: 'username: pass'. Example: 'david: 123'")
		return False
	if len(password) == 0:
		print(f"Warning - Skipping configure creds of: '{creds}' becuase they are not in the right format\npassword is of length 0\nShould be: 'username: pass'. Example: 'david: 123'")
		return False
	return True

def validate_permissions(permissions):
	if not permissions:
		return False
	if ':' not in permissions:
		print(f"Warning - Skipping configure permissions of: '{permissions}' becuase they are not in the right format\n Should be: 'name/version@user/channel: user1, user2, user3'. Example: '*/*@*/*: demo' ")
		return False
	username, password = permissions.split(":")
	if len(username) == 0:
		print(f"Warning - Skipping configure permissions of: '{permissions}' becuase they are not in the right format\nusername is of length 0\nShould be: 'name/version@user/channel: user1, user2, user3'. Example: '*/*@*/*: demo'")
		return False
	if len(password) == 0:
		print(f"Warning - Skipping configure permissions of: '{permissions}' becuase they are not in the right format\npassword is of length 0\nShould be: 'name/version@user/channel: user1, user2, user3'. Example: '*/*@*/*: demo'")
		return False
	return True


def configure_conan_server_conf_file(config):
	global conan_server_creds_list
	global conan_server_read_permissions
	global conan_server_write_permissions
	conan_server_creds_list = convert_to_list(conan_server_creds_list)
	conan_server_read_permissions = convert_to_list(conan_server_read_permissions)
	conan_server_write_permissions = convert_to_list(conan_server_write_permissions)
	if conan_server_creds_list:
		print("Configuring Creds")
		for creds in conan_server_creds_list:
			if not validate_creds(creds):
				continue
			username, password = creds.split(":")
			if not config.has_option("users", username):
				print(f"Adding username: '{username}'")
				config["users"][username] = password

	if conan_server_read_permissions:
		print("Configuring Permissions")
		for creds in conan_server_creds_list:
			if not validate_creds(creds):
				continue
			username, password = creds.split(":")
			if not config.has_option("users", username):
				print(f"Adding username: '{username}'")
				config["users"][username] = password


def main():
	print(f"Configuring conan-server config ini file: '{conan_server_config_file}' ")
	check_params()
	default_server_settings = get_default_server_settings()
	config = read_conf_file()
	config = validate_config(config, default_server_settings)
	config = configure_conan_server_conf_file(config)
	print(f"Finished configuring conan-server config ini file: '{conan_server_config_file}' ")


# Start
if __name__ == "__main__":
	main()