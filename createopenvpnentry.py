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

device = Device(identifier)
new_hostname = device.hostname+"."+device.context
cur.execute("SELECT INET_ATON(ip) from devices WHERE context = 'vpn' ORDER BY INET_ATON(ip) DESC Limit 1")
new_ip = str(ipaddress.ip_address(cur.fetchone()[0]+1))

sql = "INSERT INTO devices (identifier,ip,context,hostname,description,connection) VALUES ('%s','%s','vpn','%s','%s','openvpn')"
print(sql,(device.get_fqdn(),new_ip,new_hostname,device.description)
try:
    cur.execute(sql)
    db.commit()
except:
    db.rollback()
