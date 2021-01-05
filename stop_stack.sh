
# Pass "clean" to clean the old storage 
#  and start a new fresh stack
#


echo Stopping conan-server stack..

docker-compose down

echo Finished stopping conan-server stack

if [ "$1" == "clean" ]; then 
	echo Cleaning conan-server stack
	rm -rf conan-server-data
	echo Done cleaning
fi