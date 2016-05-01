#!/bin/bash
basepath="$(dirname "$(readlink -f "$0")")"
"$basepath/generatedokuwikidevices.py" > /var/www/dokuwiki/data/pages/network/devices_generated.txt
"$basepath/generatedokuwikicontexts.py" > /var/www/dokuwiki/data/pages/network/contexts_generated.txt
"$basepath/generatedokuwikicnames.py" > /var/www/dokuwiki/data/pages/network/cnames_generated.txt
