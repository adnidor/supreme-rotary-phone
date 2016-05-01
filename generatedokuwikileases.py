#!/usr/bin/python3
from datetime import datetime as dt
import socket

print("====== Leases ======")
print("DO NOT EDIT - This file is generated automatically")
print()
print("^Gültig bis ^MAC ^IP ^Hostname ^")

with open("/var/lib/misc/dnsmasq.leases") as leasefile:
    for leasestr in leasefile:
        lease = leasestr.split()
        valid_till = dt.fromtimestamp(int(lease[0])).strftime('%Y-%m-%d %H:%M:%S')
        mac = lease[1]
        ip = lease[2]
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "error while resolving"
        print("|"+valid_till+"|"+mac+"|"+ip+"|"+hostname+"|")
