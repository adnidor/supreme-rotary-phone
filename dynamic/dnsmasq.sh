#!/bin/bash
"$(dirname "$(dirname "$(readlink -f "$0")")")/generateconfig/generatednsmasqconf.py" > /etc/dhcphosts
/usr/bin/service dnsmasq restart &> /dev/null
