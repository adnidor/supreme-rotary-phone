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

required_fields = ["context","ip","identifier","description","hostname","devicetype","connection","type"]

if not all(field in submitted for field in required_fields):
    print("Es fehlen Eingaben")
    exit(1)

context = submitted.getfirst("context").lower()
ip = submitted.getfirst("ip")
identifier = submitted.getfirst("identifier").lower()
description = submitted.getfirst("description")
hostname = submitted.getfirst("hostname").lower()
devicetype = submitted.getfirst("devicetype").lower()
connection = submitted.getfirst("connection").lower()
type = submitted.getfirst("type").lower()

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

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
print("Type: "+type)
print("<br />")


sql = "INSERT INTO devices (identifier, ip, hostname, description, context, devicetype, connection, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)";

print(sql % (identifier,ip,hostname,description,context,devicetype,connection,type))

#try:
#    cur.execute(sql, (identifier,ip,hostname,description,context,devicetype,connection,type))
#    db.commit()
#except:
#    db.rollback()
#    print("Error")

#exec("sudo /home/yannik/networkmanagement/update.sh");
