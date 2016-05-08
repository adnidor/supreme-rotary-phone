#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()



print("====== VLANs ======")
print("DO NOT EDIT - This file is generated automatically")
print("^Id ^Name ^")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT name,id FROM vlans")

vlans = cur.fetchall()

for vlan in vlans:
    name  = vlan[0]
    id = vlan[1]
    print("|"+str(id)+"|"+name+"|")


