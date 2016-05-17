#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

DOMAIN=server_config.domain

class Context:
    def __init__(self, name=None, id=None):
        if name is None and id is None:
            return
        if name is not None:
            self.name = name
            db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
            cur = db.cursor()
            cur.execute("SELECT i,iprange,description,dhcp FROM contexts WHERE name = %s", (name,))
            result = cur.fetchone()
            if result is None:
                raise KeyError("Context not found")
            self.id = result[0]
            self.iprange = result[1]
            self.description = result[2]
            self.dhcp = True if result[3] == 1 else False
        elif id is not None:
            self.id = id
            db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
            cur = db.cursor()
            cur.execute("SELECT name,iprange,description,dhcp FROM contexts WHERE i = %s", (id,))
            result = cur.fetchone()
            if result is None:
                raise KeyError("Context not found")
            self.name = result[0]
            self.iprange = result[1]
            self.description = result[2]
            self.dhcp = True if result[3] == 1 else False
    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.description

class Device:
    def __init__(self, identifier):
        if identifier is None:
            return
        self.identifier = identifier
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        cur.execute("SELECT ip,context,hostname,altname,description,type,devicetype,connection, devicetypes.name,ports FROM devices LEFT JOIN devicetypes ON devices.devicetype = devicetypes.number WHERE identifier = %s", (identifier,))
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
        self.ports = result[9].split(",")
        if self.ports == ['']:
            self.ports = []
        self.ports_str = []
        if self.connection == "wifi":
            for port in self.ports:
                cur.execute("SELECT ssid FROM wifis WHERE id=%s",(port,))
                self.ports_str.append(cur.fetchone()[0])
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

    def write_to_db(self):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        cur.execute("SELECT 1 FROM devices WHERE identifier = %s",(self.identifier,))
        exists = len(cur.fetchall()) > 0
        if exists:
            sql = "UPDATE devices SET ip = %s, context = %s, hostname = %s, altname = %s, description = %s, devicetype = %s, connection = %s WHERE identifier = %s"
        else:
            sql = "INSERT INTO devices SET ip = %s, context = %s, hostname = %s, altname = %s, description = %s, devicetype = %s, connection = %s, identifier = %s"
        try:
            cur.execute(sql, (self.ip, self.context, self.hostname, self.altname, self.description, self.devicetype, self.connection, self.identifier))
            db.commit()
        except:
            db.rollback()

def get_devices_where(statement,vars=None):
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()
    sql = "SELECT identifier FROM devices WHERE "+statement
    if vars is None:
        cur.execute(sql)
    else:
        cur.execute(sql,vars)
    results = cur.fetchall()
    devices = []
    for result in results:
        devices.append(Device(result[0]))
    return devices

def get_all_devices():
    return get_devices_where("1=1")

def get_contexts_where(statement,vars=None):
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()
    sql = "SELECT i FROM contexts WHERE "+statement
    if vars is None:
        cur.execute(sql)
    else:
        cur.execute(sql,vars)
    results = cur.fetchall()
    contexts = []
    for result in results:
        contexts.append(Context(id=result[0]))
    return contexts

def get_all_contexts():
    return get_contexts_where("1=1")
        
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


