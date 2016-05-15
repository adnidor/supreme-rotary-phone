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

if "device" not in cgi.FieldStorage():
    print("Kein Gerät angegeben")
    exit(1)
device = cgi.FieldStorage().fetchone("device")

cur.execute("SELECT identifier,ip,hostname,altname,description,type,devicetypes.name,connection FROM devices LEFT JOIN devicetypes ON devices.devicetype = devicetypes.number WHERE identifier = %s ORDER BY INET_ATON(ip)", (device,))
result = cur.fetchone()

identifier =    device[0]
ip =            device[1]
hostname =      device[2]
altname =       device[3]
description =   device[4]
type =          device[5]
devicetype =    device[6]
connection =    device[7]

print("<html><head>")
print("<title>"+description+"</title>")
print("</head><body>")
print("<h1>Detailansicht</h1>")
print("<h2>"+description+"</h2>")
print("Identifier: "+identifier)
print("<br />")
print("IP-Adresse: "+ip)
print("<br />")
print("Hostname: "+hostname)
print("<br />")
print("Alternativer Hostname: "+altname)
print("<br />")
print("Adresstyp: "+type)
print("<br />")
print("Gerätetyp: "+devicetype)
print("<br />")
print("Verbindungtyp: "+connection)

print("</body></html>")
