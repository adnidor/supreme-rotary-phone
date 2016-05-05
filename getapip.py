#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import sys
from helpers import get_fqdn
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <ap>")
    exit(1)
ap = sys.argv[1] #erster Parameter

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT devices.ip FROM aps, devices WHERE aps.device = devices.identifier AND aps.name = '"+ap+"'")
aps = cur.fetchall()[0][0]

print(apip)
