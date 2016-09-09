#!/usr/bin/python3
#coding=utf-8
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

aps = helpers.AccessPoint.get_all()
wifis = helpers.WifiNetwork.get_all()
devices = helpers.Device.get_where("connection = 'wifi'")

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
print(".disabled { color: grey; }")
print("</style>")
print("</head><body>")
print("<h1>WLAN</h1>")

print("<h2>Netzwerke</h2>")
print("<a href=show_wifi_passwords.cgi>Passwörter</a>")
print("<table>")
print("<tr><th>SSID</th><th>VLAN</th><th>Access Control</th><th>Versteckt?</th><th>Modus</th><th>Access Points</th><th>Whitelist?</th></tr>")
for wifi in wifis:
    vlan = wifi.vlan.name if wifi.vlan is not None else "None"
    hidden = "Ja" if wifi.hidden else "Nein"
    whitelist = "Ja" if wifi.whitelist else "Nein"
    #if encryption == "passphrase" and authorized:
    #    encryption += " ("+wifi[6]+")"
    if wifi.enabled:
        print("<tr>")
    else:
        print("<tr class=disabled>")
    print("<td>%s</td>"%(wifi.ssid,))
    print("<td>%s</td>"%(vlan,))
    print("<td>%s</td>"%(wifi.authmethod,))
    print("<td>%s</td>"%(hidden,))
    print("<td>%s</td>"%(wifi.mode,))
    print("<td>")
    print("<ul class=aplist>")
    for ap in aps:
        if ap in wifi.aps:
            print("<li><input type='checkbox' disabled checked />%s</li>"%ap.name)
        else:
            print("<li><input type='checkbox' disabled />%s</li>"%ap.name)
    print("</ul>")
    print("<td>%s</td>"%(whitelist,))
    print("</td>")
    print("</tr>")
print("</table>")

print("<h2>Access Points</h2>")
print("<table><tr><th>ID</th><th>Name</th><th>Kanal</th><th>Model</th><th>Wlanstatus</th></tr>")
for ap in aps:
    wifi_status = "Aktiviert" if ap.wifi_enabled else "Deaktiviert"
    print("<tr>")
    print("<td>%s</td>"%(str(ap.id),))
    print("<td>%s</td>"%(ap.name,))
    print("<td>%s</td>"%(str(ap.channel),))
    print("<td>%s</td>"%(ap.model,))
    print("<td>%s</td>"%(wifi_status,))
    print("</tr>")
print("</table>")

def get_link_details(device):
    return "<a href=show_device.cgi?device="+device+">Details</a>"

print("<h2>Geräte</h2>")
print("<table><tr><th>Name</th><th>Kontext</th><th>MAC</th><th>Netzwerke</th><th></th></tr>")
for device in devices:
    print("<tr>")
    print("<td>%s</td>"%(device.description,))
    print("<td>%s</td>"%(device.context.description,))
    print("<td>%s</td>"%(device.identifier,))
    print("<td><ul class=netlist>")
    for port in device.ports_str:
        print("<li>"+port+"</li>")
    print("</ul></td>")
    print("<td>%s</td>"%(get_link_details(device.identifier),))
    print("</tr>")
print("</table>")

print("</body></html>")
