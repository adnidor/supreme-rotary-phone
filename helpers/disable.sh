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

if [ -L $en_path/$service ]
then
    rm $en_path/$service
    echo "found $service"
else
    echo "didn't do anything"
fi
