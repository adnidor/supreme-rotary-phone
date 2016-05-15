#!/bin/bash
if [[ $(whoami) != "root" ]]
then
    echo not root, exiting
    exit 1
fi

logger -t srp "starting update..."
basepath="$(dirname "$(readlink -f "$0")")"
logger -t srp "basepath: $basepath"
for file in $basepath/dynamic/*
do  
    logger -t srp "executing $file"
    $file
done
date +"%s" > /etc/networkmanagement/last_update
