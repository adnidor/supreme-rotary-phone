#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
mkdir -p "$basepath/tmp"
for ap in $("$basepath/listaps.py")
do
	"$basepath/generateowrtwireless.py" $ap > "$basepath/tmp/$ap.wireless"
	"$basepath/generateowrtnetwork.py" $ap > "$basepath/tmp/$ap.network"
done

