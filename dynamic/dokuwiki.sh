#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")/generateconfig"
"$basepath/generatedokuwikidevices.py" > /var/www/dokuwiki/data/pages/network/devices_generated.txt
"$basepath/generatedokuwikicontexts.py" > /var/www/dokuwiki/data/pages/network/contexts_generated.txt
"$basepath/generatedokuwikicnames.py" > /var/www/dokuwiki/data/pages/network/cnames_generated.txt
"$basepath/generatedokuwikiwifis.py" > /var/www/dokuwiki/data/pages/network/wifis_generated.txt
"$basepath/generatedokuwikivlans.py" > /var/www/dokuwiki/data/pages/network/vlans_generated.txt
