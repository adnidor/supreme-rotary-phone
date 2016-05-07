#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <ap>")
    exit(1)
ap = sys.argv[1] #erster Parameter

print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT id, vlans, mvlan, interfaces FROM aps WHERE name = '"+ap+"'")
result = cur.fetchall()[0]
apid = result[0]
vlans = result[1].split(",")
mvlan = result[2]
ifaces = result[3].split(",")

print("config interface 'loopback'")
print("    option ifname 'lo'")
print("    option proto 'static'")
print("    option ipaddr '127.0.0.1'")
print("    option netmask '255.0.0.0'")
print()

for vlan in vlans:
    print("config interface 'vlan"+vlan+"'")
    ifname= "option ifname '"
    for iface in ifaces:
        ifname=ifname+iface+"."+vlan+" "
    ifname=ifname.strip()+"'"
    print("    "+ifname)
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
