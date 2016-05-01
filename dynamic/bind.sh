#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
"$basepath/generatenamedconflocal.py" > /etc/bind/internaldomain.conf
for context in $("$basepath/listcontexts.py")
do
	"$basepath/generatebindaconfig.py" $context > /etc/bind/db.${context}.forward
	"$basepath/generatebindptrconfig.py" $context > /etc/bind/db.${context}.reverse
done
"$basepath/generatebindmacconfig.py" > /etc/bind/db.mac

/usr/bin/service bind9 reload &> /dev/null
