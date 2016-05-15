#!/usr/bin/python3
#coding=utf-8
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


print("Content-type: text/html; charset=UTF-8")
print()


def get_link_edit(device):
    return "<a href=adddevice_form.cgi?action=edit&device="+device+">Edit</a>"

def get_link_details(device):
    return "<a href=show_device.cgi?device="+device+">Details</a>"

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

sql = "SELECT name,description,iprange FROM contexts"
cur.execute(sql)
contexts = cur.fetchall()

devices = {}

for context in contexts:
    cur.execute("SELECT identifier,ip,hostname,description FROM devices WHERE context = %s ORDER BY INET_ATON(ip)", (context[0],))
    devices[context[0]] = cur.fetchall()

print("<html><head>")
print("<title>Geräte</title>")
print("<style>")
print("th,td {")
print("border: 1px solid;")
print("}")
print("table { border-collapse: collapse; }")
print("tr:nth-child(even) {")
print("background-color: white;")
print("}")
print("tr:nth-child(odd) {")
print("background-color: silver;")
print("}")
print("</style>")
print("</head><body>")
print("<h1>Geräte</h1>")
for context in contexts:
    print("<h2>"+context[1]+" ("+context[2]+")</h2>")
    if len(devices[context[0]]) > 0:
        print("<table>")
        print("<tr><th>Identifier</th><th>IP-Adresse</th><th>Hostname</th><th>Beschreibung</th><th>Aktion</th></tr>")
        for device in devices[context[0]]:
            identifier =    device[0]
            ip =            device[1]
            hostname =      device[2]
            description =   device[3]
            print("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s %s</td></tr>" % (identifier,ip,hostname,description,get_link_edit(identifier),get_link_details(identifier)))
        print("</table>")

print("</body></html>")
