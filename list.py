#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import sys
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

targets = {"aps":{"table":"aps", "column":"name"},"contexts":{"table":"contexts","column":"name"}}

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <target>")
    exit(1)
target = sys.argv[1] #erster Parameter

if target not in targets:
   print("invalid target")
   exit(1)

cur.execute("SELECT "+targets[target]["column"]+" FROM "+targets[target]["table"])
results = cur.fetchall()

for result in results:
    print(result[0])
