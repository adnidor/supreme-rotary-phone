#!/usr/bin/python3
import ipaddress as ipa
import socket, struct
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import helpers
import server_config

print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

contexts = helpers.Context.get_all()

for context in contexts:
    devices = helpers.Device.get_where("context=%s AND type = 'dhcp'",(context.id,))
    if len(devices) is 0 and not context.dhcp:
        continue
    print()
    print("#"+context.description)
    network = ipa.ip_network(context.iprange)
    naddr= str(network.network_address)
    baddr= str(network.broadcast_address)
    first_host = socket.inet_ntoa(struct.pack("!L", struct.unpack("!L", socket.inet_aton(naddr))[0]+1))
    last_host = socket.inet_ntoa(struct.pack("!L", struct.unpack("!L", socket.inet_aton(baddr))[0]-1))

    if context.dhcp:
        print("dhcp-range="+first_host+","+last_host+",1h")
    else:
        print("dhcp-range="+naddr+",static,1h")

    for device in devices:
        tag = "internet" if device.internet else "nointernet"
        print("dhcp-host="+device.identifier+","+device.ip+",set:"+tag+" #"+device.description+" ("+device.hostname+")")


