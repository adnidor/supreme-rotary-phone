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

cur.execute("SELECT id, name, channel, model FROM aps")
aps = cur.fetchall()

cur.execute("SELECT aps,ssid, authmethod, vlans.name, hidden, mode, whitelist FROM wifis LEFT JOIN vlans ON wifis.vlan = vlans.id")
wifis = cur.fetchall()

cur.execute("SELECT identifier,devices.description,contexts.description,ports FROM devices JOIN contexts ON devices.context = contexts.name WHERE connection = 'wifi' ORDER BY INET_ATON(devices.ip)")
devices = cur.fetchall()

common_name = os.getenv("SSL_CLIENT_S_DN_CN")
authorized = helpers.is_user_authorized(common_name)

print("<html><head>")
print("<title>WLAN</title>")
print("<style>")
print("th,td { border: 1px solid; }")
print("table { border-collapse: collapse; }")
print("tr:nth-child(even) { background-color: white; }")
print("tr:nth-child(odd) { background-color: silver; }")
print(".aplist { list-style: none; padding: 0; margin: 0; }")
print(".netlist { margin: 0; }")
print("</style>")
print("</head><body>")
print("<h1>WLAN</h1>")


def get_ap_name(apid):
    cur.execute("SELECT name FROM aps WHERE id = %s", (apid,))
    return cur.fetchone()[0]

print("<h2>Netzwerke</h2>")
print("<table>")
print("<tr><th>SSID</th><th>VLAN</th><th>Access Control</th><th>Versteckt?</th><th>Modus</th><th>Access Points</th><th>Whitelist?</th></tr>")
for wifi in wifis:
    apids = wifi[0].split(",")
    ssid = wifi[1]
    encryption = wifi[2]
    vlan = wifi[3] if wifi[3] is not None else "None"
    hidden = "Ja" if wifi[4] == 1 else "Nein"
    mode = wifi[5] 
    whitelist = "Ja" if wifi[6] == 1 else "Nein"
    #if encryption == "passphrase" and authorized:
    #    encryption += " ("+wifi[6]+")"
    print("<tr>")
    print("<td>%s</td>"%(ssid,))
    print("<td>%s</td>"%(vlan,))
    print("<td>%s</td>"%(encryption,))
    print("<td>%s</td>"%(hidden,))
    print("<td>%s</td>"%(mode,))
    print("<td>")
    print("<ul class=aplist>")
    for ap in aps:
        id = ap[0]
        name = ap[1]
        if str(id) in apids:
            print("<li><input type='checkbox' disabled checked />%s</li>"%name)
        else:
            print("<li><input type='checkbox' disabled />%s</li>"%name)
    print("</ul>")
    print("<td>%s</td>"%(whitelist,))
    print("</td>")
    print("</tr>")
print("</table>")

print("<h2>Access Points</h2>")
print("<table><tr><th>Name</th><th>Kanal</th><th>Model</th></tr>")
for ap in aps:
    id = ap[0]
    name = ap[1]
    channel = ap[2]
    model = ap[3]
    print("<tr>")
    print("<td>%s</td>"%(name,))
    print("<td>%s</td>"%(str(channel),))
    print("<td>%s</td>"%(model,))
    print("</tr>")
print("</table>")

def get_link_details(device):
    return "<a href=show_device.cgi?device="+device+">Details</a>"

print("<h2>Geräte</h2>")
print("<table><tr><th>Name</th><th>Kontext</th><th>MAC</th><th>Netzwerke</th><th></th></tr>")
for device in devices:
    mac = device[0]
    description = device[1]
    context = device[2]
    link = get_link_details(mac)
    ports = device[3].split(",")
    print("<tr>")
    print("<td>%s</td>"%(description,))
    print("<td>%s</td>"%(context,))
    print("<td>%s</td>"%(mac,))
    print("<td><ul class=netlist>")
    for port in ports:
        cur.execute("SELECT ssid FROM wifis WHERE id=%s",(port,))
        result = cur.fetchone()
        if result is None:
            continue
        print("<li>"+result[0]+"</li>")
    print("</ul></td>")
    print("<td>%s</td>"%(link,))
    print("</tr>")
print("</table>")

print("</body></html>")
