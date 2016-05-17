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

if "device" not in cgi.FieldStorage():
    print("Kein Gerät angegeben")
    exit(1)
id = cgi.FieldStorage().getfirst("device")

device = helpers.Device(id)

print("<html><head>")
print("<title>"+device.description+"</title>")
print("<style>")
print(".netlist { margin: 0; }")
print("</style>")
print("</head><body>")
print("<h1>Detailansicht</h1>")
print("<h2>"+device.description+" ("+device.fqdn+")</h2>")
print("<table>")
print("<tr><td>Identifier:</td><td>"+device.identifier+"</td></tr>")
print("<tr><td>IP-Adresse:</td><td>"+device.ip+"</td></tr>")
print("<tr><td>Hostname:</td><td>"+device.hostname+"</td></tr>")
print("<tr><td>Alternativer Hostname:</td><td>"+device.altname+"</td></tr>")
print("<tr><td>Adresstyp:</td><td>"+device.type+"</td></tr>")
print("<tr><td>Gerätetyp:</td><td>"+device.devicetype_str+"</td></tr>")
print("<tr><td>Verbindungtyp:</td><td>"+device.connection+"</td></tr>")
if device.connection == "wifi":
    print("<tr><td>Netzwerke</td>")
    print("<td><ul class=netlist>")
    for port in device.ports_str:
        print("<li>"+port+"</li>")
    print("</ul></td>")

print("</table>")

print("</body></html>")
