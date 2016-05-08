#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()



print("====== WLAN-Netzwerke ======")
print("DO NOT EDIT - This file is generated automatically")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT id, name, channel FROM aps")

aps = cur.fetchall()

cur.execute("SELECT aps,ssid, authmethod, vlans.name, hidden, mode FROM wifis LEFT JOIN vlans ON wifis.vlan = vlans.id")
wifis = cur.fetchall()

for ap in aps:
    id = ap[0]
    name = ap[1]
    channel = ap[2]
    print("====="+name+"=====")
    print("Kanal: "+str(channel))
    print("^SSID ^VLAN ^Verschlüsselung ^Versteckt? ^Modus ^")
    for wifi in wifis:
        if str(id) not in wifi[0].split(","):
            continue
        ssid = wifi[1]
        encryption = wifi[2]
        vlan = wifi[3] if wifi[3] is not None else "None"
        hidden = "Ja" if wifi[4] == 1 else "Nein"
        mode = wifi[5]
        print("|"+ssid+"|"+vlan+"|"+encryption+"|"+hidden+"|"+mode+"|")

