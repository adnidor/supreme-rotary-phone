#!/usr/bin/python3
import mysql.connector as ms
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config

print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database") #must be first non-import line, waits for fifo to be opened

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()
cur.execute("SELECT identifier, ip, contexts.description, devices.description, hostname FROM devices JOIN contexts ON devices.context = contexts.name WHERE devices.type='dhcp' ORDER BY INET_ATON(ip)")

for row in cur.fetchall():
    print(row[0]+","+row[1]+" #"+row[3]+" ("+row[4]+") von "+row[2])

