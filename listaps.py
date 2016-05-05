#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from helpers import get_fqdn
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()


DOMAIN=server_config.domain

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT name FROM aps")
aps = cur.fetchall()

for ap in aps:
    name = ap[0]
    print(name)
