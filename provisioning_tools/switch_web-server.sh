#!/bin/bash

TMP=`mktemp /tmp/switch_web-server.XXXXXXXXXX`
CURL='curl -q -m 10'
source /etc/kolla/admin-openrc.sh 

openstack server list > $TMP
IP1=`grep $1 $TMP | sed 's/^.*| demo-net=\(.*\), .*$/\1/'`
IP2=`grep $2 $TMP | sed 's/^.*| demo-net=\(.*\), .*$/\1/'`

rm $TMP

web-server() {
	for i in `seq 15`
	do
		ANSWER=`$CURL $1 2> /dev/null`
		if [ $? = 0 ]
		then
			echo "Web-server's answer:" $ANSWER
			return 0
		else
			sleep 30
		fi
	done
	echo web-server unavailable
	return 1
}

echo openstack server start $2
openstack server start $2

for i in `seq 10`
do
	#if ping -c 5 -q $IP2 > /dev/null 2>&1
	if web-server http://$IP2:8000 > /dev/null 2>&1
	then
		echo openstack server stop $1
		openstack server stop $1
		break
	else
		sleep 30
	fi
done

if ! ping -c 5 -q $IP2 > /dev/null 2>&1
then
	echo $2 is not working
       	exit
fi

#sudo ed /etc/hosts >/dev/null <<END
sudo ed /etc/hosts <<END
/ *web-server *$
s/^\(.*[[:alnum:]]\)[[:space:]]\+web-server[[:space:]]*$/\1/
1
/$IP2
s/\([[:alnum:]]\)[[:space:]]*$/\1 web-server/
wq
END

web-server http://web-server:8000

$CURL http://$IP1:8000 > /dev/null 2>&1 && echo $1 \($IP2\) is working

$CURL http://$IP2:8000 > /dev/null 2>&1 && echo $2 \($IP2\) is working
