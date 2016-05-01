#!/bin/bash
if [[ $(whoami) != "root" ]]
then
echo not root, exiting
exit 1
fi

basepath="$(dirname "$(readlink -f "$0")")"
"$basepath/dynamicbindconfig.sh"
"$basepath/dynamicdhcphosts.sh"
"$basepath/dynamicdokuwiki.sh"

