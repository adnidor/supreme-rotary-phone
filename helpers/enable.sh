#!/bin/bash
service=$1
if [ $( basename $(pwd) ) = dynamic ]
then
    avail_path="."
    en_path="enabled"

elif [ -d dynamic ]
then
    avail_path="dynamic"
    en_path="dynamic/enabled"

else
    echo "Couldn't find path"
    exit 1
fi

if [ -f $avail_path/$service ]
then
    ln -s ../$service $en_path/$service
    echo "found $service"
elif [ -f $avail_path/$service.sh ]
then
    ln -s ../$service.sh $en_path/$service
    echo "found $service.sh"
else
    echo "didn't do anything"
fi
