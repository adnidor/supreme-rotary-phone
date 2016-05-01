#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()


print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT name, dhcp, description, iprange FROM contexts")

contexts = cur.fetchall()

for context in contexts:
    contextname = context[0]
    contextdesc = context[2]
    contextdhcp = context[1]
    contextrange = context[3]
    cur.execute("SELECT identifier, ip, description, hostname FROM devices WHERE context='"+contextname+"' AND type='dhcp' ORDER BY INET_ATON(ip)")
    print()
    print("#"+contextdesc)
    if contextdhcp is 1:
        network = ipa.ip_network(contextrange)
        naddr= str(network.network_address)
        baddr= str(network.broadcast_address)
        first_host = socket.inet_ntoa(struct.pack("!L", struct.unpack("!L", socket.inet_aton(naddr))[0]+1))
        last_host = socket.inet_ntoa(struct.pack("!L", struct.unpack("!L", socket.inet_aton(baddr))[0]-1))
    
        print("dhcp-range="+first_host+","+last_host+",12h")
    for row in cur.fetchall():
        mac = row[0]
        ip = row[1]
        description = row[2]
        hostname = row[3]
        print("dhcp-host="+mac+","+ip+" #"+description+" ("+hostname+")")

