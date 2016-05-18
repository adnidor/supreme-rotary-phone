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
import cgi
cgitb.enable()

print("Content-type: text/html")
print()
db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

submitted = cgi.FieldStorage()
edit = False
if submitted.getfirst("action") == "edit" :
    edit = True
    dev = submitted.getfirst("device")
    if dev is None:
        print("Error")
        exit(1)
    device = helpers.Device(dev)

context = device.context if edit else None
identifier = device.identifier if edit else ""
ip = device.ip if edit else None
hostname = device.hostname if edit else ""
altname = device.altname if edit else None
description = device.description if edit else ""
type = device.type if edit else "dhcp"
devicetype = device.devicetype if edit else 0
connection = device.connection if edit else "ethernet"

contexts = helpers.get_all_contexts()

sql = "SELECT name, number FROM devicetypes";
cur.execute(sql)
devicetypes = cur.fetchall()


calling_ip = os.getenv('REMOTE_ADDR')
#mac = subprocess.check_output(["/opt/get_mac_from_ip.sh", calling_ip], universal_newlines=True).strip()
mac = "aa:bb:cc:dd:ee:ff"

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
action="adddevice.cgi" if not edit else "editdevice.cgi"
print("<form action="+action+" method=POST>")
print("Context: <select id='context' name='context'>")
for cnxt in contexts:
    if edit and cnxt == context:
        print("<option value="+str(cnxt.id)+" selected>"+cnxt.description+"</option>")
    else:
        print("<option value="+str(cnxt.id)+">"+cnxt.description+"</option>")
print("</select> <a href=# onclick=prefill()>prefill</a>")
print("<br />")
print("Identifier: <input type=text name=identifier id=mac value='"+identifier+"' />")
print("<br />")
if edit:
    print("IP: <input type=text name=ip value='"+ip+"' />")
    print("<br />")
print("Description: <input type=text name=description value='"+description+"'/>")
print("<br />")
print("Hostname: <input type=text name=hostname value='"+hostname+"'/>")
print("<br />")
print("Devicetype: <select name='devicetype'>")
for devtype in devicetypes:
    if edit and devtype[1] == devicetype:
        print("<option value="+str(devtype[1])+" selected>"+devtype[0]+"</option>")
    else:
        print("<option value="+str(devtype[1])+">"+devtype[0]+"</option>")
print("</select>")
print("<br />")
print("Connection: <input type=text name=connection value='"+connection+"' />")
print("<br />")
print("Type: <input type=text name=type value='"+type+"' />")
print("<br />")
print("<input type=submit />")
print("</form>")
print("</body>")
print("</html>")
