#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys, os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import models

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <ap>")
    exit(1)
ap = sys.argv[1] #erster Parameter



print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT id, channel, radiussecret, radiusserver, model FROM aps WHERE name = '"+ap+"'")
result = cur.fetchall()[0]
apid = result[0]
channel = result[1]
radiussecret = result[2]
radiusserver = result[3]
model = result[4]

print("config wifi-device 'radio0'")
print("    option type 'mac80211'")
print("    option hwmode '11g'")
print("    option htmode 'HT40'")
print("    option path '"+models.wireless_path[model]+"'")
print("    option country 'DE'")
print("    option channel '"+str(channel)+"'")
print()

cur.execute("SELECT aps,ssid, authmethod, vlan, hidden, passphrase, mode,whitelist FROM wifis")
wifis = cur.fetchall()

cur.execute("SELECT identifier FROM devices WHERE connection = 'wifi'")
devices = cur.fetchall()

for wifi in wifis:
    aps = wifi[0].split(",")
    if str(apid) not in aps:
        continue
    ssid = wifi[1]
    authmethod = wifi[2]
    vlan = wifi[3]
    hidden = True if wifi[4] == 1 else False
    passphrase = wifi[5]
    mode = wifi[6]
    whitelist = wifi[7]
    print("config wifi-iface")
    print("    option device 'radio0'")
    print("    option mode '"+mode+"'")
    print("    option ssid '"+ssid+"'")
    if hidden:
        print("    option hidden '1'")
    if vlan > 0:
        print("    option network 'vlan"+str(vlan)+"'")
    if authmethod == 'none':
        print("    option encryption 'none'")
    elif authmethod == "radius":
        print("    option encryption 'wpa2'")
        print("    option auth_server '"+radiusserver+"'")
        print("    option auth_secret '"+radiussecret+"'")
    elif authmethod == "passphrase":
        print("    option encryption 'psk2'")
        print("    option key '"+passphrase+"'")
    if whitelist:
        maclist = ""
        for device in devices:
            maclist += device[0]+" "
        print("    option maclist '"+maclist.strip()+"'")
        print("    option macfilter 'allow'")
    print()
