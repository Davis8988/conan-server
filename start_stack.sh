echo ""

# Pass "clean" to clean the old storage 
#  and start a new fresh stack
#


# During setup of conan-server it's important to assign the ip address of the executing host
#  this section below tries to extract the ip address. It must have the right interface name though..
#  run 'ifconfig' and see what is the desired interface name

#ADAPTER_NAME=enp0s8
#ADAPTER_NAME=eth0
DEFAULT_ADAPTER_NAME=ens192
export ADATPER_NAME_TO_EXTRACT_FROM=${ADAPTER_NAME:-$DEFAULT_ADAPTER_NAME}
echo "Attempting to retrieve ip address of interface: '${ADATPER_NAME_TO_EXTRACT_FROM}' to configure it in conan-server config file"
export HOST_IP_ADDR=$(ip -4 addr show ${ADATPER_NAME_TO_EXTRACT_FROM} | grep -oP "(?<=inet )[\d\.]+(?=/)")
if [ -z "$HOST_IP_ADDR" ]; then 
    echo""; echo "Error - Failed to retrieve ip address of interface: '${ADATPER_NAME_TO_EXTRACT_FROM}'"; echo " Maybe it's not the right interface name?" 
    echo " Execute 'ifconfig' and see what is the right interface name"
    echo "  and re-execute this script again. Example: "; echo ""; echo "  ADAPTER_NAME=eth08 ./start_stack.sh"; echo ""
    if [ ! -z "$ADAPTER_NAME" ]; then exit 1; else echo "Continuing anyway.. "; echo ""; fi 
else
    echo "Found host ip: '$HOST_IP_ADDR'. Configuring it in the conan-server config file"
fi

if [ "$1" == "clean" ]; then 
	echo Cleaning conan-server stack
	rm -rf conan-server-data
	echo Done cleaning
fi

echo ""

echo Starting conan-server stack..

docker-compose up -d

echo Finished starting conan-server stack
