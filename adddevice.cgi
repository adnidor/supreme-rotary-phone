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

if not ("context" in submitted and "identifier" in submitted and "description" in submitted and "hostname" in submitted and "devicetype" in submitted and "connection" in submitted):
    print("Es fehlen Eingaben")
    exit(1)

context = submitted.getfirst("context").lower()
identifier = submitted.getfirst("identifier").lower()
description = submitted.getfirst("description")
hostname = submitted.getfirst("hostname").lower()
devicetype = submitted.getfirst("devicetype").lower()
connection = submitted.getfirst("connection").lower()

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

sql = "SELECT ip from devices WHERE context = '"+context+"' ORDER BY INET_ATON(ip) DESC Limit 1";
cur.execute(sql)
ip = str(ipaddress.ip_address(cur.fetchone()[0])+1)

print("Context: "+context)
print("<br />")
print("Id: "+identifier)
print("<br />\n")
print("IP: "+ip)
print("<br />\n")
print("Description: "+description)
print("<br />\n")
print("Hostname: "+hostname)
print("<br />\n")
print("Devicetype: "+devicetype)
print("<br />\n")
print("Connection: "+connection)


sql = "INSERT INTO devices (identifier, ip, hostname, description, context) VALUES ('$mac', '$ip', '$hostname', '$description', '$context')";

print(sql)

#exec("sudo /home/yannik/networkmanagement/update.sh");

