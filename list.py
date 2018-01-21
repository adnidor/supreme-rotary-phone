#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import sys
import helpers
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

targets = {
           "aps":           {"table":"aps", "column":"name", "where":"1", "convert":lambda x: x},
           "apips":         {"table":"aps", "column":"device", "where":"1", "convert":lambda x: helpers.Device(x).ip},
           "apids":         {"table":"aps", "column":"id", "where":"1", "convert":lambda x: x},
           "owrtaps":       {"table":"aps", "column":"name", "where":"model = 'wr841n'", "convert":lambda x: x},
           "contexts":      {"table":"contexts","column":"name", "where":"1", "convert":lambda x: x},
           "contextids":    {"table":"contexts","column":"i", "where":"1", "convert":lambda x: x},
           "identifiers":   {"table":"devices","column":"identifier", "where":"1", "convert":lambda x: x},
           "devices":       {"table":"devices","column":"identifier", "where":"1" ,"convert":lambda x: helpers.Device(x).fqdn},
           "backupdevices": {"table":"devices","column":"identifier", "where":"backup = 1" ,"convert":lambda x: helpers.Device(x).fqdn}
          }

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <target>")
    exit(1)
target = sys.argv[1] #erster Parameter

if target not in targets:
    print("unknown target")
    exit(1)

cur.execute("SELECT "+targets[target]["column"]+" FROM "+targets[target]["table"]+" WHERE "+targets[target]["where"])
results = cur.fetchall()

for result in results:
    result = targets[target]["convert"](result[0])
    if result is not None:
        print(result)
