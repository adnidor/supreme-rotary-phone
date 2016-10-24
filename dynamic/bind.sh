#!/bin/bash
basepath="$(dirname "$(dirname "$(readlink -f "$0")")")"
"$basepath/generateconfig/generatenamedconflocal.py" > /etc/bind/internaldomain.conf
for context in $("$basepath/list.py" "contextids")
do
	"$basepath/generateconfig/generatebindaconfig.py" "$context" > /etc/bind/$("$basepath/get_zonefile_name.py" "$context" forward)
	"$basepath/generateconfig/generatebindptrconfig.py" "$context" > /etc/bind/$("$basepath/get_zonefile_name.py" "$context" reverse)
done
"$basepath/generateconfig/generatebindmacconfig.py" > /etc/bind/db.mac

/bin/systemctl reload bind9 &> /dev/null
