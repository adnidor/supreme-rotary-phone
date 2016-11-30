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

submitted = cgi.FieldStorage()

print("Content-type: text/html")
print()

if not ("context" in submitted and "identifier" in submitted and "description" in submitted and "hostname" in submitted and "devicetype" in submitted and "connection" in submitted and "type" in submitted):
    print("Es fehlen Eingaben")
    exit(1)

context = submitted.getfirst("context").lower()
identifier = submitted.getfirst("identifier").lower()
description = submitted.getfirst("description")
hostname = submitted.getfirst("hostname").lower()
devicetype = submitted.getfirst("devicetype").lower()
connection = submitted.getfirst("connection").lower()
internet = 1 if bool(submitted.getvalue("internet")) else 0
alwayson = 1 if bool(submitted.getvalue("alwayson")) else 0
type = submitted.getfirst("type").lower()

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

sql = "SELECT ip from devices WHERE context = %s ORDER BY INET_ATON(ip) DESC Limit 1";
cur.execute(sql, (context,))
ip = str(ipaddress.ip_address(cur.fetchone()[0])+1)

print("Context: "+context)
print("<br />")
print("Id: "+identifier)
print("<br />")
print("IP: "+ip)
print("<br />")
print("Description: "+description)
print("<br />")
print("Hostname: "+hostname)
print("<br />")
print("Devicetype: "+devicetype)
print("<br />")
print("Connection: "+connection)
print("<br />")
print("Internet: "+internet)
print("<br />")
print("Always-On: "+alwayson)
print("<br />")
print("Type: "+type)
print("<br />")


sql = "INSERT INTO devices (identifier, ip, hostname, description, context, devicetype, connection, type, internet, alwayson) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";

print(sql % (identifier,ip,hostname,description,context,devicetype,connection,type,internet,alwayson))

try:
    cur.execute(sql, (identifier,ip,hostname,description,context,devicetype,connection,type,internet,alwayson))
    db.commit()
    print("Successfully added. <a href=update.cgi>Update</a> <a href=.>Home</a>")
except:
    db.rollback()
    print("Error")

