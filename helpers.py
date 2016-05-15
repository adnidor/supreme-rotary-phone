#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()


DOMAIN=server_config.domain

def get_fqdn(identifier):
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()

    cur.execute("SELECT hostname,context FROM devices WHERE identifier='"+identifier+"'")
    devices = cur.fetchall()
    devicename = devices[0][0]
    context = devices[0][1]
    if context == "root":
        contextstr = "."
    else:
        contextstr = "."+context+"."
    return devicename+contextstr+DOMAIN

def get_secs_since_update():
    file = open("/etc/networkmanagement/last_update")
    lastchange = int(file.readline())
    import time
    timestamp = int(time.time())
    return timestamp-lastchange
