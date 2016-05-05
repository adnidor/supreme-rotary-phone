#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
for ap in $("$basepath/listaps.py")
do
	"$basepath/generateowrtwireless.py" $ap > "$basepath/$ap.wireless"
	"$basepath/generateowrtnetwork.py" $ap > "$basepath/$ap.network"
done

