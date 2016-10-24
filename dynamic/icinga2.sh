#!/bin/bash
"$(dirname "$(dirname "$(readlink -f "$0")")")/generateconfig/generateicinga2hosts.py" > "$("$(dirname "$(dirname "$(readlink -f "$0")")")/get_config_option.py" icinga2_hosts)"
"$(dirname "$(dirname "$(readlink -f "$0")")")/generateconfig/generateicinga2hostgroups.py" > "$("$(dirname "$(dirname "$(readlink -f "$0")")")/get_config_option.py" icinga2_hostgroups)"
/bin/systemctl reload icinga2
