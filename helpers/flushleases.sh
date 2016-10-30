#!/bin/bash
if [[ $(whoami) != "root" ]]
then
echo not root, exiting
exit 1
fi

/usr/bin/service dnsmasq stop
rm /var/lib/misc/dnsmasq.leases
/usr/bin/service dnsmasq start
