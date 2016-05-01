#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import ipaddress as ipa
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()


print("#DO NOT TOUCH - This file is generated automagically")

DOMAIN = server_config.domain+"."

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT name,iprange FROM contexts")
contexts = cur.fetchall()

for context in contexts:
    contextstr = context[0]
    if contextstr == "root":
        contextstring = ""
    else:
        contextstring = contextstr+"."
    network = ipa.ip_network(context[1])
    reverse_record = ".".join((".".join(str(network.network_address).split(".")[::-1])+'.in-addr.arpa').split(".")[1:]) #dark magic - do not touch
    print("zone \""+contextstring+DOMAIN+"\" {")
    print("type master;")
    print("file \"/etc/bind/db."+contextstr+".forward\";")
    print("};")
    print("zone \""+reverse_record+"\" {")
    print("type master;")
    print("file \"/etc/bind/db."+contextstr+".reverse\";")
    print("};")

print("zone \"mac."+DOMAIN+"\" {")
print("type master;")
print("file \"/etc/bind/db.mac\";")
print("};")
