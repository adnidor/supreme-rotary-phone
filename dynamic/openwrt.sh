#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
mkdir -p "$basepath/tmp"
for ap in $("$basepath/list.py" "aps")
do
	"$basepath/generateconfig/generateowrtwireless.py" "$ap" > "$basepath/tmp/$ap.wireless.new"
	"$basepath/generateconfig/generateowrtnetwork.py" "$ap" > "$basepath/tmp/$ap.network.new"
    ip="$("$basepath/getapip.py" "$ap")"
    dirty=0
    diff "$basepath/tmp/$ap.wireless.new" "$basepath/tmp/$ap.wireless" > /dev/null
    if [ $? -ne 0 ]
    then
        scp -q "$basepath/tmp/$ap.wireless.new" root@$ip:/etc/config/wireless
        mv "$basepath/tmp/$ap.wireless.new" "$basepath/tmp/$ap.wireless"  
        dirty=1
    fi
    diff "$basepath/tmp/$ap.network.new" "$basepath/tmp/$ap.network" > /dev/null
    if [ $? -ne 0 ]
    then
        scp -q "$basepath/tmp/$ap.network.new" root@$ip:/etc/config/network
        mv "$basepath/tmp/$ap.network.new" "$basepath/tmp/$ap.network"  
        dirty=1
    fi
    if [ $dirty -eq 1 ]; then
        ssh root@$ip 'uci commit network; uci commit wireless; wifi'
    fi
done

