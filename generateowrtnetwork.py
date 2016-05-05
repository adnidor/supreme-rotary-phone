#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys
from importlib.machinery import SourceFileLoader

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <ap>")
    exit(1)
ap = sys.argv[1] #erster Parameter

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()


print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT id, vlans, mvlan, interface FROM aps WHERE name = '"+ap+"'")
result = cur.fetchall()[0]
apid = result[0]
vlans = result[1].split(",")
mvlan = result[2]
iface = result[3]

print("config interface 'loopback'")
print("    option ifname 'lo'")
print("    option proto 'static'")
print("    option ipaddr '127.0.0.1'")
print("    option netmask '255.0.0.0'")
print()

for vlan in vlans:
    print("config interface 'vlan"+vlan+"'")
    print("    option ifname '"+iface+"."+vlan+"'")
    print("    option type 'bridge'")
    if vlan == str(mvlan):
        print("    option proto 'dhcp'")
    else:
        print("    option proto 'none'")
    print()


try:
    manual = open("/etc/networkmanagement/"+ap+".network.manual", "r")
    print(manual.read())
except IOError:
    print()