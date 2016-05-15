#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
import ipaddress
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers
import cgi
import cgitb
cgitb.enable()

print("Content-type: text/html")
print()

def get_link(device):
    return "<a href=adddevice_form.cgi?edit=true&device="+device+">Edit</a>"

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

sql = "SELECT name,description FROM contexts"
cur.execute(sql)
contexts = cur.fetchall()

devices = {}

for context in contexts:
    cur.execute("SELECT identifier,ip,hostname,altname,description,type,devicetypes.name,connection FROM devices LEFT JOIN devicetypes ON devices.devicetype = devicetypes.number WHERE context = %s ORDER BY INET_ATON(ip)", (context[0],))
    devices[context[0]] = cur.fetchall()

print("<html><head>")
print("<title>Geräte</title>")
print("</head><body>")
print("<h1>Geräte</h1>")
for context in contexts:
    print("<h2>"+context[1]+"</h2>")
    print("<table>")
    print("<tr><th>Identifier</th><th>IP-Adresse</th><th>Hostname</th><th>Altname</th><th>Beschreibung</th><th>Typ</th><th>Gerätetyp</th><th>Verbindung</th></tr>")
    for device in devices[context[0]]:
        identifier =    device[0]
        ip =            device[1]
        hostname =      device[2]
        altname =       device[3]
        description =   device[4]
        type =          device[5]
        devicetype =    device[6]
        connection =    device[7]
        print("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (identifier,ip,hostname,altname,description,type,devicetype,connection,get_link(identifier)))
    print("</table>")
