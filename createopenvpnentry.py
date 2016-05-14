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

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <identifier>")
    exit(1)
identifier = sys.argv[1]

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT context,hostname,description FROM devices WHERE identifier=%s", (identifier,))
results = cur.fetchall()

if len(results) == 0:
    print("device not found")
    exit(1)
elif len(results) > 1:
    print("multiple results found, aborting")
    exit(1)

new_id = helpers.get_fqdn(identifier)
context = results[0][0]
hostname = results[0][1]
description = results[0][2]
new_hostname = hostname+"."+context
cur.execute("SELECT INET_ATON(ip) from devices WHERE context = 'vpn' ORDER BY INET_ATON(ip) DESC Limit 1")
new_ip = str(ipaddress.ip_address(cur.fetchone()[0]+1))

sql = "INSERT INTO devices (identifier,ip,context,hostname,description,connection) VALUES ('"+new_id+"','"+new_ip+"','vpn','"+new_hostname+"','"+description+"','openvpn')"
print(sql)
try:
    cur.execute(sql)
    db.commit()
except:
    db.rollback()
