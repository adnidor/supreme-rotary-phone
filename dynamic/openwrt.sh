#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
mkdir -p "$basepath/tmp"
for ap in $("$basepath/list.py" "aps")
do
	"$basepath/generateconfig/generateowrtwireless.py" "$ap" > "$basepath/tmp/$ap.wireless"
	"$basepath/generateconfig/generateowrtnetwork.py" "$ap" > "$basepath/tmp/$ap.network"
    ip="$("$basepath/getapip.py" "$ap")"
    scp -q "$basepath/tmp/$ap.wireless" root@$ip:/etc/config/wireless
    scp -q "$basepath/tmp/$ap.network" root@$ip:/etc/config/network
    ssh root@$ip 'uci commit network; uci commit wireless; wifi'
    rm "$basepath/tmp/$ap.network"
    rm "$basepath/tmp/$ap.wireless"
done

