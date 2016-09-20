#!/bin/bash
"$(dirname "$(dirname "$(readlink -f "$0")")")/generateconfig/generatednsmasqconf.py" > "$("$(dirname "$(dirname "$(readlink -f "$0")")")/get_config_option.py" dnsmasq_config)"
/usr/bin/service dnsmasq restart &> /dev/null
