#!/bin/bash
basepath="$(dirname "$(readlink -f "$0")")"
for ap in $("$basepath/list.py" "apips")
do
    ssh root@$ap 'reboot'
done

