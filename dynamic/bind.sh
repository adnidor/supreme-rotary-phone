#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
"$basepath/generateconfig/generatenamedconflocal.py" > /etc/bind/internaldomain.conf
for context in $("$basepath/list.py" "contexts")
do
	"$basepath/generateconfig/generatebindaconfig.py" $context > /etc/bind/db.${context}.forward
	"$basepath/generateconfig/generatebindptrconfig.py" $context > /etc/bind/db.${context}.reverse
done
"$basepath/generateconfig/generatebindmacconfig.py" > /etc/bind/db.mac

/usr/bin/service bind9 reload &> /dev/null
