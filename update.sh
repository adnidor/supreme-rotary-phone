#!/bin/bash
basepath="$(dirname "$(readlink -f "$0")")"
"$basepath/dynamicbindconfig.sh"
"$basepath/dynamicdhcphosts.sh"
"$basepath/dynamicdokuwiki.sh"

