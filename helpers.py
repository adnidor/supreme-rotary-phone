#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import socket,struct
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

DOMAIN=server_config.domain

class EqualityMixin:
    def __eq__(self, other):
        return (type(other) is type(self)) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

class Context(EqualityMixin):
    def __init__(self, name=None, id=None):
        if name is None and id is None:
            return
        if name is not None and type(name) == type("fdsfs"):
            self.name = name
            db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
            cur = db.cursor()
            cur.execute("SELECT i,iprange,description,dhcp,parent,email FROM contexts WHERE name = %s", (name,))
            result = cur.fetchone()
            if result is None:
                raise KeyError("Context not found")
            self.id = result[0]
            self.iprange = result[1]
            self.description = result[2]
            self.dhcp = True if result[3] == 1 else False
            self.parent = None if result[4] is None else Context(id=result[4])
            self.email = result[5]
        elif id is not None:
            self.id = id
            db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
            cur = db.cursor()
            cur.execute("SELECT name,iprange,description,dhcp,parent,email FROM contexts WHERE i = %s", (id,))
            result = cur.fetchone()
            if result is None:
                raise KeyError("Context not found")
            self.name = result[0]
            self.iprange = result[1]
            self.description = result[2]
            self.dhcp = True if result[3] == 1 else False
            self.parent = None if result[4] is None else Context(id=result[4])
            self.email = result[5]
    def __repr__(self):
        return "<Context "+str(self.id)+">"

    def __str__(self):
        return self.description

    def __eq__(self, other):
        return (self.id == other.id) and (self.name == other.name)

    def __hash__(self):
        return self.id

    def get_devices(self):
        return get_devices_where("context = %s",(str(self.id),))

    def is_root(self):
        return self.parent is None

    def get_domain_part(self):
        if self.is_root():
            return ""
        else:
            return "."+self.name+self.parent.get_domain_part()

    def get_zonefile_name(self, suffix):
        if self.is_root():
            return "db.root."+suffix
        else:
            return "db"+self.get_domain_part()+"."+suffix

    @classmethod
    def get_where(cls, statement,vars=None):
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
            contexts.append(cls(result[0]))
        return contexts

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

class Device(EqualityMixin):
    def __init__(self, identifier):
        if identifier is None:
            return
        self.identifier = identifier
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = """SELECT
                    devices.ip,
                    devices.context,
                    devices.hostname,
                    devices.altname,
                    devices.description,
                    devices.type,
                    devices.devicetype,
                    devices.connection,
                    devicetypes.name,
                    devices.ports,
                    devices.internet
                 FROM devices 
                    LEFT JOIN devicetypes ON devicetypes.number = devices.devicetype
                 WHERE
                    identifier = %s
              """
        cur.execute(sql, (identifier,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("Device not found")
        self.ip = result[0]
        self.context = Context(id=result[1])
        self.hostname = result[2]
        self.altname = result[3]
        self.description = result[4]
        self.type = result[5]
        self.devicetype = result[6]
        self.connection = result[7]
        self.devicetype_str = result[8]
        self.ports = result[9].split(",") if self.connection == "wifi" else []
        self.port = result[9].split("/") if self.connection == "ethernet" else ['']
        self.portraw = result[9]
        self.internet = True if result[10] == 1 else False
        self.port_str = ""
        if self.ports == ['']:
            self.ports = []
        self.ports_str = []
        if self.connection == "wifi":
            for port in self.ports:
                cur.execute("SELECT ssid FROM wifis WHERE id=%s",(port,))
                self.ports_str.append(cur.fetchone()[0])
        elif self.connection == "ethernet" and self.port != ['']:
            sql = "SELECT description FROM switches WHERE id=%s"
            cur.execute(sql,(self.port[0],))
            result = cur.fetchone()[0]
            self.port_str = "Port %s auf %s"%(self.port[1],result)
        self.fqdn = self.get_fqdn()

    @classmethod
    def get_where(cls, statement,vars=None):
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
            devices.append(cls(result[0]))
        return sorted(devices, key=Device.get_key)

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

    def __str__(self):
        return self.get_fqdn()

    def __repr__(self):
        return "<Device "+self.identifier+">"

    def __eq__(self, other):
        return (self.identifier == other.identifier)

    def get_fqdn(self):
        return self.hostname+self.context.get_domain_part()+"."+DOMAIN

    def get_key(x):
        return struct.unpack("!I", socket.inet_aton(x.ip))[0] #IP as number

    def write_to_db(self):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        cur.execute("SELECT 1 FROM devices WHERE identifier = %s",(self.identifier,))
        exists = len(cur.fetchall()) > 0
        if exists:
            sql = "UPDATE devices SET ip = %s, context = %s, hostname = %s, altname = %s, description = %s, devicetype = %s, connection = %s, ports = %s WHERE identifier = %s"
        else:
            sql = "INSERT INTO devices SET ip = %s, context = %s, hostname = %s, altname = %s, description = %s, devicetype = %s, connection = %s, identifier = %s, ports = %s"
        try:
            cur.execute(sql, (self.ip, self.context, self.hostname, self.altname, self.description, self.devicetype, self.connection, self.identifier, ",".join(self.ports)))
            db.commit()
        except:
            db.rollback()

    def __hash__(self):
        return hash(self.identifier)

class WifiNetwork(EqualityMixin):
    def __init__(self, id):
        self.id = int(id)
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = """SELECT
                    ssid,
                    vlan,
                    authmethod,
                    aps,
                    hidden,
                    passphrase,
                    mode,
                    whitelist,
                    enabled
                 FROM wifis 
                 WHERE
                    id = %s
              """
        cur.execute(sql, (id,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("Network not found")
        self.ssid = result[0]
        self.vlan = Vlan(result[1]) if result[1] != 0 else None
        self.authmethod = result[2]
        self.aps = [AccessPoint(i) for i in result[3].split(",")]
        self.hidden = True if result[4] == 1 else False
        self.passphrase = result[5] if result[5] != "" else None
        self.mode = result[6]
        self.whitelist = True if result[7] == 1 else False
        self.enabled = True if result[8] == 1 else False

    def __str__(self):
        return self.ssid

    def __repr__(self):
        return "<WifiNetwork "+str(self.id)+">"

    @classmethod
    def get_where(cls, statement,vars=None):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = "SELECT id FROM wifis WHERE "+statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql,vars)
        results = cur.fetchall()
        wifis = []
        for result in results:
            wifis.append(cls(result[0]))
        return wifis

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

class Vlan(EqualityMixin):
    def __init__(self,id):
        self.id = int(id)
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = """SELECT
                    name
                 FROM vlans 
                 WHERE
                    id = %s
              """
        cur.execute(sql, (id,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("Vlan not found")
        self.name = result[0]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Vlan "+str(self.id)+">"

    @classmethod
    def get_where(cls, statement,vars=None):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = "SELECT id FROM vlans WHERE "+statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql,vars)
        results = cur.fetchall()
        vlans = []
        for result in results:
            vlans.append(cls(result[0]))
        return vlans

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

class AccessPoint(EqualityMixin):
    def __init__(self,id):
        self.id = int(id)
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = """SELECT
                    device,
                    channel,
                    radiussecret,
                    radiusserver,
                    name,
                    vlans,
                    mvlan,
                    switch,
                    model,
                    interfaces,
                    wifi_enabled
                 FROM aps 
                 WHERE
                    id = %s
              """
        cur.execute(sql, (id,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("AP not found")
        self.device = Device(result[0])
        self.channel = result[1]
        self.radiussecret = result[2]
        self.radiusserver = result[3]
        self.name = result[4]
        self.vlans = [Vlan(i) for i in result[5].split(",")]
        self.mvlan = Vlan(result[6])
        self.switch = result[7]
        self.model = result[8]
        self.interfaces = result[9].split(",")
        self.wifi_enabled = True if result[10] == 1 else False

    def __repr__(self):
        return "<AccessPoint "+str(self.id)+">"

    @classmethod
    def get_where(cls, statement,vars=None):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = "SELECT id FROM aps WHERE "+statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql,vars)
        results = cur.fetchall()
        aps = []
        for result in results:
            aps.append(cls(result[0]))
        return aps

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

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
    return sorted(devices, key=Device.get_key)

def get_all_devices():
    return get_devices_where("1")

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
    return get_contexts_where("1")
        
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

def get_root_context():
    return get_contexts_where("parent IS NULL")[0]

def get_device_from_fqdn(fqdn):
    if not fqdn.endswith(DOMAIN):
        return None
    hostcntxt = strip_end(fqdn, "."+DOMAIN)
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()
    contexts = get_all_contexts()
    devcontext = None
    host = None
    for context in contexts:
        if hostcntxt.endswith(context.name):
            devcontext = context
            host = strip_end(hostcntxt,"."+devcontext.name)
            break
    if devcontext is None:
        devcontext = get_root_context()
        host = strip_end(hostcntxt, ".")
    cur.execute("SELECT identifier FROM devices WHERE (hostname = %s OR altname = %s) AND context = %s",(host,host,devcontext.id))
    results = cur.fetchall()
    if len(results) != 1:
        return None
    return Device(results[0][0])


