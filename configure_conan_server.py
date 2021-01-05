
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
	default_server_settings_config = configparser.ConfigParser()
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

	default_server_settings_config.add_section("server")
	for k,v in default_server_section_data.items():
		default_server_settings_config["server"][k] = v

	default_read_permissions_section_data = {
		'*/*@*/*' : '*'
	}

	default_server_settings_config.add_section("read_permissions")
	for k,v in default_read_permissions_section_data.items():
		default_server_settings_config["read_permissions"][k] = v

	return default_server_settings_config


def convert_to_list(string_var, delimiter):
	if not string_var:
		return None
	converted_list = string_var.split(delimiter)
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
	global conan_server_config_file
	try:
		config = configparser.ConfigParser()
		print(f"Reading config file")
		config.read(conan_server_config_file)
		return config
	except BaseException as error_msg:
		print(f"Error - Failed reading conan-server config ini file: '{conan_server_config_file}'\n{error_msg}")
		sys.exit(1)


def fix_missing_settings_with_defaults(config, default_server_settings):
	print("Fixing missing sections and entries in config file with defaults")
	for sec_name in required_sections:
		if not default_server_settings.has_section(sec_name):
			continue
		section = default_server_settings[sec_name]
		if not config.has_section(sec_name):
			section = default_server_settings[sec_name]
			print(f"Adding default missing section & settings: {sec_name}")
			config.add_section(section)
			continue
		for k,v in section.items():
			if not config.has_option(sec_name, k):
				print(f"Adding default missing configuration: {sec_name}.{k}={v}")
				k = k.strip()
				v = v.strip()
				config[sec_name][k] = v

	return config


def validate_config(config):
	print("Validating config file")
	for sec_name in required_sections:
		if not config.has_section(sec_name):
			print(f"Error - Conan config file: '{conan_server_config_file}' is missing section: '{sec_name}'\nCannot continue with missing configurations")
			sys.exit(1)
	return config


def validate_creds(creds):
	error_msg = "The creds are not in the right format\n Should be: 'username: pass'. Example: 'david: 123'"
	if not creds:
		return False
	if ':' not in creds:
		print(f"Warning - Skipping configure creds of: '{creds}' - Missing ':'\n{error_msg} ")
		return False
	username, password = creds.split(":")
	if len(username) == 0:
		print(f"Warning - Skipping configure creds of: '{creds}' - username is of length = 0 (empty)\n{error_msg}")
		return False
	if len(password) == 0:
		print(f"Warning - Skipping configure creds of: '{creds}' - password is of length = 0 (empty)\n{error_msg}")
		return False
	return True

def validate_permissions(permissions):
	error_msg = "The permissions are not in the right format\n Should be: 'name/version@user/channel: user1, user2, user3'. Example: '*/*@*/*: demo' "
	if not permissions:
		return False
	if ':' not in permissions:
		print(f"Warning - Skipping configure permissions of: '{permissions}' - Missing ':'\n{error_msg}")
		return False
	if '@' not in permissions:
		print(f"Warning - Skipping configure permissions of: '{permissions}' - Missing '@'\n{error_msg}")
		return False
	prefix_scope, postfix_scope = permissions.split(":")
	if len(prefix_scope) == 0:
		print(f"Warning - Skipping configure permissions of: '{permissions}'  - The prefix scope before '@': '{prefix_scope}' is of length = 0 (empty)\n{error_msg}")
		return False
	if '/' not in prefix_scope:
		print(f"Warning - Skipping configure permissions of: '{permissions}'  - The prefix scope before '@': '{prefix_scope}' is missing '/' sign\n{error_msg}")
		return False
	if len(postfix_scope) == 0:
		print(f"Warning - Skipping configure permissions of: '{permissions}'  - The postfix scope after '@': '{postfix_scope}' is of length = 0 (empty)\n{error_msg}")
		return False
	if '/' not in postfix_scope:
		print(f"Warning - Skipping configure permissions of: '{permissions}'  - The postfix scope after '@': '{postfix_scope}' is missing '/' sign\n{error_msg}")
		return False
	for ps in [prefix_scope, postfix_scope]:
		a,b = ps.split("/")
		if len(a) == 0 or len(b) == 0:
			print(f"Warning - Skipping configure permissions of: '{permissions}'  - One of the scopes between '/' sign of: '{ps}' is of length = 0 (empty)\n{error_msg}")
			return False
	return True


def configure_conan_server_conf_file(config):
	global conan_server_creds_list
	global conan_server_read_permissions
	global conan_server_write_permissions
	conan_server_creds_list = convert_to_list(conan_server_creds_list, ";")
	conan_server_read_permissions = convert_to_list(conan_server_read_permissions, ";")
	conan_server_write_permissions = convert_to_list(conan_server_write_permissions, ";")
	if conan_server_creds_list:
		print("Configuring Creds")
		for creds in conan_server_creds_list:
			if not validate_creds(creds):
				continue
			username, password = creds.split(":")
			if not config.has_option("users", username):
				username = username.strip()
				password = password.strip()
				print(f"Adding username: '{username}'")
				config["users"][username] = password

	if conan_server_read_permissions:
		print("Configuring Read Permissions")
		for permissions in conan_server_read_permissions:
			if not validate_permissions(creds):
				continue
			prefix_scope, postfix_scope = permissions.split(":")
			if not config.has_option("read_permissions", prefix_scope):
				print(f"Adding read permissions: '{permissions}'")
				prefix_scope = prefix_scope.strip()
				postfix_scope = postfix_scope.strip()
				config["read_permissions"][prefix_scope] = postfix_scope

	if conan_server_write_permissions:
		print("Configuring Write Permissions")
		for permissions in conan_server_write_permissions:
			if not validate_permissions(creds):
				continue
			prefix_scope, postfix_scope = permissions.split(":")
			if not config.has_option("write_permissions", prefix_scope):
				print(f"Adding write permissions: '{permissions}'")
				prefix_scope = prefix_scope.strip()
				postfix_scope = postfix_scope.strip()
				config["write_permissions"][prefix_scope] = postfix_scope

	return config


def write_conan_server_conf_file(config):
	try:
		with open(conan_server_config_file, 'w') as configfile:
			config.write(configfile)
	except BaseException as error_msg:
		print(f"Error - Failed to write conan-server config ini file: '{conan_server_config_file}'\n{error_msg}")
		sys.exit(1)


def main():
	print(f"Configuring conan-server config ini file: '{conan_server_config_file}' ")
	check_params()
	config = read_conf_file()
	default_server_settings = get_default_server_settings()
	config = configure_conan_server_conf_file(config)
	config = fix_missing_settings_with_defaults(config, default_server_settings)
	validate_config(config)
	write_conan_server_conf_file(config)
	print(f"Finished configuring conan-server config ini file: '{conan_server_config_file}' ")


# Start
if __name__ == "__main__":
	main()