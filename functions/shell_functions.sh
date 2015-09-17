function getPrivateIp() {
	PRIVATE_IP=`ifconfig | grep "inet addr" | awk -F: '{print $2}' | awk '{print $1}' | head -1`
	echo $PRIVATE_IP
}

