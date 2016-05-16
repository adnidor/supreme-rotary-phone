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
    if len(devices) != 1:
        return None
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

def is_user_authorized(cn):
    userfile = open("/etc/networkmanagement/authorized_users")
    for line in userfile:
        if cn in line:
            return True
    return False

def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]

def get_identifier_from_fqdn(fqdn):
    if not fqdn.endswith(DOMAIN):
        return None
    hostcntxt = strip_end(fqdn, "."+DOMAIN)
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()
    cur.execute("SELECT name FROM contexts")
    contexts = cur.fetchall()
    devcontext = None
    host = None
    for context in contexts:
        if hostcntxt.endswith(context[0]):
            devcontext = context[0]
            host = strip_end(hostcntxt,"."+devcontext)
            break
    if devcontext is None:
        devcontext = "root"
        host = strip_end(hostcntxt, ".")
    cur.execute("SELECT identifier FROM devices WHERE (hostname = %s OR altname = %s) AND context = %s",(host,host,devcontext))
    results = cur.fetchall()
    if len(results) != 1:
        return None
    return results[0][0]

