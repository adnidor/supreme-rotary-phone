#!/usr/bin/python3
#coding=utf-8
import struct,socket
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers
import cgitb
cgitb.enable()


print("Content-type: text/html; charset=UTF-8")
print()

def get_link_edit(device):
    return "<a href=adddevice_form.cgi?action=edit&device="+device+">Edit</a>"

def get_link_details(device):
    return "<a href=show_device.cgi?device="+device+">Details</a>"

contexts = helpers.Context.get_all()
devices = {}
for context in contexts:
    devices[context] = context.get_devices()

print("<html><head>")
print("<title>Geräte</title>")
print("<style>")
print("th,td { border: 1px solid; }")
print("table { border-collapse: collapse; }")
print("tr:nth-child(even) { background-color: white; }")
print("tr:nth-child(odd) { background-color: silver; }")
print("</style>")
print("</head><body>")
print("<h1>Geräte</h1>")
for context in contexts:
    print("<h2>"+context.description+" ("+context.iprange+")</h2>")
    if len(devices[context]) > 0:
        print("<table>")
        print("<tr><th>Identifier</th><th>IP-Adresse</th><th>Hostname</th><th>Beschreibung</th><th>Aktion</th></tr>")
        for device in devices[context]:
            print("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s %s</td></tr>" % (device.identifier,device.ip,device.hostname,device.description,get_link_edit(device.identifier),get_link_details(device.identifier)))
        print("</table>")

print("</body></html>")
