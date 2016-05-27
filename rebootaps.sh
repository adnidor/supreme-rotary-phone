#!/bin/bash
basepath="$(dirname "$(readlink -f "$0")")"
for ap in $("$basepath/list.py" "aps")
do
    ip="$("$basepath/getapip.py" "$ap")"
    ssh root@$ip 'reboot'
done

