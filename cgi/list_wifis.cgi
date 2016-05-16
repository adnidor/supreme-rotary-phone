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

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT id, name, channel FROM aps")
aps = cur.fetchall()

cur.execute("SELECT aps,ssid, authmethod, vlans.name, hidden, mode FROM wifis LEFT JOIN vlans ON wifis.vlan = vlans.id")
wifis = cur.fetchall()

cur.execute("SELECT identifier,devices.description,contexts.description FROM devices JOIN contexts ON devices.context = contexts.name WHERE connection = 'wifi' ORDER BY INET_ATON(devices.ip)")
devices = cur.fetchall()

print("<html><head>")
print("<title>WLAN</title>")
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
print("<h1>WLAN</h1>")

print("<h2>Access Points</h2>")
print("<table><tr><th>Name</th><th>Kanal</th></tr>")
for ap in aps:
    id = ap[0]
    name = ap[1]
    channel = ap[2]
    print("<tr>")
    print("<td>%s</td>"%(name,))
    print("<td>%s</td>"%(str(channel),))
    print("</tr>")
print("</table>")

def get_ap_name(apid):
    cur.execute("SELECT name FROM aps WHERE id = %s", (apid,))
    return cur.fetchone()[0]

print("<h2>Netzwerke</h2>")
print("<table>")
print("<tr><th>SSID</th><th>VLAN</th><th>Access Control</th><th>Versteckt?</th><th>Modus</th><th>Access Points</th></tr>")
for wifi in wifis:
    apids = wifi[0].split(",")
    aps = ""
    for apid in apids:
        if apid == "":
            continue
        aps += get_ap_name(apid)+" "
    if aps == "":
        aps = "Keine"
    ssid = wifi[1]
    encryption = wifi[2]
    vlan = wifi[3] if wifi[3] is not None else "None"
    hidden = "Ja" if wifi[4] == 1 else "Nein"
    mode = wifi[5] 
    print("<tr>")
    print("<td>%s</td>"%(ssid,))
    print("<td>%s</td>"%(vlan,))
    print("<td>%s</td>"%(encryption,))
    print("<td>%s</td>"%(hidden,))
    print("<td>%s</td>"%(mode,))
    print("<td>%s</td>"%(aps,))
    print("</tr>")
print("</table>")

def get_link_details(device):
    return "<a href=show_device.cgi?device="+device+">Details</a>"

print("<h2>Geräte</h2>")
print("<table><tr><th>Name</th><th>Kontext</th><th>MAC</th><th></tr>")
for device in devices:
    mac = device[0]
    description = device[1]
    context = device[2]
    link = get_link_details(mac)
    print("<tr>")
    print("<td>%s</td>"%(description,))
    print("<td>%s</td>"%(context,))
    print("<td>%s</td>"%(mac,))
    print("<td>%s</td>"%(link,))
    print("</tr>")
print("</table>")

print("</body></html>")