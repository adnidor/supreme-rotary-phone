#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
mkdir -p "$basepath/tmp"
for ap in $("$basepath/listaps.py")
do
	"$basepath/generateowrtwireless.py" "$ap" > "$basepath/tmp/$ap.wireless"
	"$basepath/generateowrtnetwork.py" "$ap" > "$basepath/tmp/$ap.network"
    ip="$("$basepath/getapip.py" "$ap")"
    scp "$basepath/tmp/$ap.wireless" root@$ip:/etc/config/wireless
    scp "$basepath/tmp/$ap.network" root@$ip:/etc/config/network
    ssh root@$ip 'uci commit network; uci commit wireless; wifi'
    rm "$basepath/tmp/$ap.*"
done

