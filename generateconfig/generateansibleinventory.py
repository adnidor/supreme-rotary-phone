#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
from helpers import get_fqdn 

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT number, name FROM devicetypes")

devicetypes = cur.fetchall()

for type in devicetypes:
    number = type[0]
    name = type[1]
    cur.execute("SELECT identifier FROM devices WHERE devicetype="+str(number)+" ORDER BY INET_ATON(ip)")
    results = cur.fetchall()
    if len(results) is 0:
        continue
    print()
    print("["+name+"]")
    for row in results:
        identifier = row[0]
        print(get_fqdn(identifier))


