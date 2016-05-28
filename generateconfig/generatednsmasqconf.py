#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import helpers
import server_config

print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

contexts = helpers.get_all_contexts()

for context in contexts:
    devices = helpers.get_devices_where("context=%s AND type = 'dhcp'",(context.id,))
    if len(devices) is 0 and not context.dhcp:
        continue
    print()
    print("#"+context.description)
    if context.dhcp:
        network = ipa.ip_network(context.iprange)
        naddr= str(network.network_address)
        baddr= str(network.broadcast_address)
        first_host = socket.inet_ntoa(struct.pack("!L", struct.unpack("!L", socket.inet_aton(naddr))[0]+1))
        last_host = socket.inet_ntoa(struct.pack("!L", struct.unpack("!L", socket.inet_aton(baddr))[0]-1))
    
        print("dhcp-range="+first_host+","+last_host+",12h")

    for device in devices:
        print("dhcp-host="+device.identifier+","+device.ip+" #"+device.description+" ("+device.hostname+")")


