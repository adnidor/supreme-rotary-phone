#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
"$basepath/generateconfig/generatenamedconflocal.py" > /etc/bind/internaldomain.conf
for context in $("$basepath/list.py" "contexts")
do
	"$basepath/generateconfig/generatebindaconfig.py" "$context" > $("$basepath/get_zonefile_name.py" "$context" forward)
	"$basepath/generateconfig/generatebindptrconfig.py" "$context" > $("$basepath/get_zonefile_name.py" "$context" reverse)
done
"$basepath/generateconfig/generatebindmacconfig.py" > /etc/bind/db.mac

/usr/bin/service bind9 reload &> /dev/null
