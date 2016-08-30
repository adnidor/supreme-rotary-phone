#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import ipaddress as ipa
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

print("#DO NOT TOUCH - This file is generated automagically")

DOMAIN = server_config.domain+"."

contexts = helpers.get_all_contexts()

for context in contexts:
    network = ipa.ip_network(context.iprange)
    reverse_record = ".".join((".".join(str(network.network_address).split(".")[::-1])+'.in-addr.arpa').split(".")[1:]) #dark magic - do not touch
    dp = context.get_domain_part()
    dp2 = dp+"." if dp != "" else ""
    print()
    print("zone \""+dp2[1:]+DOMAIN+"\" {")
    print("type master;")
    print("file \"/etc/bind/"+context.get_zonefile_name("forward")+"\";")
    print("};")
    print()
    print("zone \""+reverse_record+"\" {")
    print("type master;")
    print("file \"/etc/bind/"+context.get_zonefile_name("reverse")+"\";")
    print("};")
    print()

print()
print("zone \"mac."+DOMAIN+"\" {")
print("type master;")
print("file \"/etc/bind/db.mac\";")
print("};")
