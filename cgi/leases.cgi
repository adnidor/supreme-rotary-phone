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

def parse_dnsmasqleases(path):
    leases_raw = [line.rstrip('\n') for line in open(path)]
    leases = []
    for lease_raw in leases_raw:
        lease_raw_split = lease_raw.split(" ")
        lease = {}
        lease['timestamp'] = lease_raw_split[0]
        lease['mac'] = lease_raw_split[1]
        lease['ip'] = lease_raw_split[2]
        try:
            lease['device'] = helpers.Device(lease['mac'])
        except KeyError:
            lease['device'] = None
        leases.append(lease)
    return leases

leases = parse_dnsmasqleases("/var/lib/misc/dnsmasq.leases")

print("<html><head>")
print("<title>DHCP-Leases</title>")
print("<style>")
print("th,td { border: 1px solid; }")
print("table { border-collapse: collapse; }")
print("tr:nth-child(even) { background-color: white; }")
print("tr:nth-child(odd) { background-color: silver; }")
print("</style>")
print("</head><body>")
print("<h1>DHCP-Leases</h1>")
print("<table>")
print("<tr><th>MAC-Adresse</th><th>IP-Adresse</th><th>Gültig bis</th><th>Gerät</th></tr>")
for lease in leases:
    link = "Nicht in Datenbank"
    if lease['device'] is not None:
        link = "<a href=show_device.cgi?device=%s>%s</a>" % (lease['device'].identifier,lease['device'].description)
    print("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (lease['mac'],lease['ip'],lease['timestamp'], link))
print("</table>")

print("</body></html>")
        
