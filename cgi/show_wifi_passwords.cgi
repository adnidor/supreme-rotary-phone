#!/usr/bin/python3
#coding=utf-8
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

wifis = helpers.WifiNetwork.get_where("authmethod = 'passphrase' OR authmethod = 'wep'")

print("<html><head>")
print("<title>WLAN-Passwörter</title>")
print("<style>")
print("th,td { border: 1px solid; }")
print("table { border-collapse: collapse; }")
print("th { background-color: silver; }")
print(".aplist { list-style: none; padding: 0; margin: 0; }")
print(".netlist { margin: 0; }")
print(".disabled { color: grey; }")
print("td.pw {")
print("    font-weight: bold;")
print("    font-family: monospace;")
print("    font-size: large;")
print("}")
print("td {")
print("    padding: 2px;")
print("    padding-left: 5px;")
print("    padding-right: 5px;")
print("}")
print("</style>")
print("</head><body>")

print("<h1>Netzwerke</h1>")
print("<table>")
print("<tr><th>SSID</th><th>Passwort</th></tr>")
for wifi in wifis:
    if wifi.enabled:
        print("<tr>")
    else:
        print("<tr class=disabled>")
    print("<td>%s</td>"%(wifi.ssid,))
    print("<td class=pw>%s</td>"%(wifi.passphrase,))
    print("</td>")
    print("</tr>")
print("</table>")

print("</body></html>")
