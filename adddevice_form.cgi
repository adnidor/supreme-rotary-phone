#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
import ipaddress
import subprocess
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

import cgitb
cgitb.enable()

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

sql = "SELECT name, iprange, description FROM contexts";
cur.execute(sql)
contexts = cur.fetchall()

sql = "SELECT name, number FROM devicetypes";
cur.execute(sql)
devicetypes = cur.fetchall()


calling_ip = os.getenv('REMOTE_ADDR')
mac = subprocess.run(["/opt/get_mac_from_ip.sh", calling_ip], stdout=subprocess.PIPE).stdout.trim()
#mac = "aa:bb:cc:dd:ee:ff"

print("Content-type: text/html")
print()
print("<html>")
print("<head>")
print("<title>Add device to network</title>")
print("<script type='text/javascript'>")
print("var mac = '"+mac+"';")
print("function prefill()")
print("{")
print("	macField = document.getElementById('mac');")
print("	macField.value = mac;")
print("}")
print("</script>")
print("</head>")
print("<body>")
print("<h1>Add device</h1>")
print("<form action=adddevice.cgi method=POST>")
print("Context: <select id='context' name='context'>")
for context in contexts:
    print("<option value="+context[0]+">"+context[2]+"</option>")
print("</select> <a href=# onclick=prefill()>prefill</a>")
print("<br />")
print("Identifier: <input type=text name=identifier id=mac />")
print("<br />")
print("Description: <input type=text name=description />")
print("<br />")
print("Hostname: <input type=text name=hostname />")
print("<br />")
print("Devicetype: <select name='devicetype'>")
for devicetype in devicetypes:
    print("<option value="+str(devicetype[1])+">"+devicetype[0]+"</option>")
print("</select>")
print("<br />")
print("Connection: <input type=text name=connection value='ethernet' />")
print("<br />")
print("Type: <input type=text name=type value='dhcp' />")
print("<br />")
print("<input type=submit />")
print("</form>")
print("</body>")
print("</html>")