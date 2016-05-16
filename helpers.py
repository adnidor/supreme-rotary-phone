#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

DOMAIN=server_config.domain

class Device:
    def __init__(self, identifier):
        self.identifier = identifier
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        cur.execute("SELECT ip,context,hostname,altname,description,type,devicetype,connection, devicetypes.name FROM devices LEFT JOIN devicetypes ON devices.devicetype = devicetypes.number WHERE identifier = %s", (identifier,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("Device not found")
        self.ip = result[0]
        self.context = result[1]
        self.hostname = result[2]
        self.altname = result[3]
        self.description = result[4]
        self.type = result[5]
        self.devicetype = result[6]
        self.connection = result[7]
        self.devicetype_str = result[8]
        self.fqdn = self.get_fqdn()

    def __str__(self):
        return self.get_fqdn()

    def __repr__(self):
        return self.identifier

    def get_fqdn(self):
        if self.context == "root":
            contextstr = "."
        else:
            contextstr = "."+self.context+"."
        return self.hostname+contextstr+DOMAIN

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

def get_device_from_fqdn(fqdn):
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
    return Device(results[0][0])


