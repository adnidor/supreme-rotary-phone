#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")/generateconfig"
"$basepath/generatedokuwikidevices.py" > "$("$basepath/../get_config_option.py" dokuwiki_dir)/devices_generated.txt"
"$basepath/generatedokuwikicontexts.py" > "$("$basepath/../get_config_option.py" dokuwiki_dir)/contexts_generated.txt"
"$basepath/generatedokuwikicnames.py" >   "$("$basepath/../get_config_option.py" dokuwiki_dir)/cnames_generated.txt"
"$basepath/generatedokuwikiwifis.py" > "$("$basepath/../get_config_option.py" dokuwiki_dir)/wifis_generated.txt"
"$basepath/generatedokuwikivlans.py" > "$("$basepath/../get_config_option.py" dokuwiki_dir)/vlans_generated.txt"
