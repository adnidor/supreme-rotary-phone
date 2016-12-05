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

    _db_fields_list = [
        "contexts.i",
        "contexts.name",
        "contexts.iprange",
        "contexts.description",
        "contexts.dhcp",
        "contexts.parent",
        "contexts.email",
        "contexts.admin_user"
    ]

    def __init__(self, errorcatcher="abcd", name=None, id=None):
        if errorcatcher != "abcd":
            raise ValueError("one of name and id must be specified")
        if name is None and id is None:
            return
        if name is not None and isinstance(name, str):
            db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
            cur = db.cursor()
            cur.execute("SELECT "+",".join(self._db_fields_list)+" FROM contexts WHERE name = %s", (name,))
            result = cur.fetchone()
            if result is None:
                raise KeyError("Context not found")
            self._assign_values(result)
        elif id is not None:
            db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
            cur = db.cursor()
            cur.execute("SELECT "+",".join(self._db_fields_list)+" FROM contexts WHERE i = %s", (id,))
            result = cur.fetchone()
            if result is None:
                raise KeyError("Context not found")
            self._assign_values(result)

    def _assign_values(self,result):
        self.id = result[0]
        self.name = result[1]
        self.iprange = result[2]
        self.description = result[3]
        self.dhcp = True if result[4] == 1 else False
        self.parent = None if result[5] is None else Context(id=result[5])
        self.email = result[6]
        self.admin_user = User(result[7])
        
    def __repr__(self):
        return "<Context "+str(self.id)+">"

    def __str__(self):
        return self.description

    def __eq__(self, other):
        return (self.id == other.id) and (self.name == other.name)

    def __hash__(self):
        return self.id

    def get_devices(self):
        return Device.get_where("context = %s",(str(self.id),))

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
        sql = "SELECT "+",".join(cls._db_fields_list)+" FROM contexts WHERE "+statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql,vars)
        results = cur.fetchall()
        contexts = []
        for result in results:
            tmp = Context()
            tmp._assign_values(result)
            contexts.append(tmp)
        return contexts

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

    @classmethod
    def get_root(cls):
        return cls.get_where("parent IS NULL")[0]

    def __contains__(self,other):
        if type(other) is Device:
            return other.context == self
        elif type(other) is str:
            result = Device.get_where("context = %s AND identifier = %s",(str(self.id), other,))
            return len(result) == 1

class Device(EqualityMixin):

    _db_fields_list = [
        "devices.ip",
        "devices.context",
        "devices.hostname",
        "devices.altname",
        "devices.description",
        "devices.type",
        "devices.devicetype",
        "devices.connection",
        "devices.ports",
        "devices.internet",
        "devices.alwayson",
        "devices.formfactor",
        "devices.identifier"
    ]
        
    def __init__(self, identifier):
        if identifier is None:
            return
        self.identifier = identifier
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = "SELECT "+",".join(self._db_fields_list+Context._db_fields_list)+"""
                 FROM devices,contexts
                 WHERE
                    devices.identifier = %s
                    AND
                    contexts.i = devices.context
              """
        cur.execute(sql, (identifier,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("Device not found")
        self._assign_values(result)

    def _assign_values(self, result):
        self.ip = result[0]
        tmp = Context()
        tmp._assign_values(result[len(self._db_fields_list):])
        self.context = tmp
        self.hostname = result[2]
        self.altname = result[3]
        self.description = result[4]
        self.type = result[5]
        self.devicetype = DeviceType(result[6])
        self.connection = result[7]
        self.ports = result[8].split(",") if self.connection == "wifi" else []
        self.port = result[8].split("/") if self.connection == "ethernet" else ['']
        self.portraw = result[8]
        self.internet = True if result[9] == 1 else False
        self.alwayson = True if result[10]== 1 else False
        self.formfactor = result[11]
        self.identifier = result[12]
        self.port_str = ""
        if self.ports == ['']:
            self.ports = []
        self.ports_str = []
        if self.connection == "wifi":
            for port in self.ports:
                pass
                #self.ports_str.append(WifiNetwork(port).ssid)
        self.fqdn = self.get_fqdn()
        

    @classmethod
    def get_where(cls, statement,vars=None):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = "SELECT "+",".join(cls._db_fields_list+Context._db_fields_list)+" FROM devices,contexts WHERE contexts.i = devices.context AND "+statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql,vars)
        results = cur.fetchall()
        devices = []
        for result in results:
            print(result)
            tmp = Device(None)
            tmp._assign_values(result)
            devices.append(tmp)
        return sorted(devices, key=Device.get_key)

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

    #use sparingly, really slow
    @classmethod
    def reliable_get_by_fqdn(cls, fqdn, list_to_search=None):
        if not isinstance(fqdn, str):
            raise TypeError

        if list_to_search is None:
            list_to_search = cls.get_all()
        for device in list_to_search:
            if fqdn == device.get_fqdn() or fqdn == device.get_alt_fqdn():
                return device

        raise KeyError("Device not found")

    def __str__(self):
        return self.get_fqdn()

    def __repr__(self):
        return "<Device "+self.identifier+">"

    def __eq__(self, other):
        return (self.identifier == other.identifier)

    def get_fqdn(self):
        return self.hostname+self.context.get_domain_part()+"."+DOMAIN

    def get_alt_fqdn(self):
        return self.altname+self.context.get_domain_part()+"."+DOMAIN

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

class DeviceType(EqualityMixin):
    def __init__(self,id):
        self.id = int(id)
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = """SELECT
                    name,
                    os,
                    platform
                 FROM devicetypes 
                 WHERE
                    number = %s
              """
        cur.execute(sql, (id,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("DeviceType not found")
        self.name = result[0]
        self.os = result[1]
        self.platform = result[2]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<DeviceType "+str(self.id)+">"

    @classmethod
    def get_where(cls, statement,vars=None):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = "SELECT number FROM devicetypes WHERE "+statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql,vars)
        results = cur.fetchall()
        devtypes = []
        for result in results:
            devtypes.append(cls(result[0]))
        return devtypes

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

class User(EqualityMixin):
    def __init__(self,id):
        self.id = int(id)
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = """SELECT
                    username,
                    name,
                    email,
                    pushover
                 FROM users 
                 WHERE
                    id = %s
              """
        cur.execute(sql, (id,))
        result = cur.fetchone()
        if result is None:
            raise KeyError("User not found")
        self.username = result[0]
        self.name = result[1]
        self.email = result[2]
        self.pushover = result[3]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<User "+str(self.id)+">"

    @classmethod
    def get_where(cls, statement,vars=None):
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        sql = "SELECT id FROM users WHERE "+statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql,vars)
        results = cur.fetchall()
        users = []
        for result in results:
            users.append(cls(result[0]))
        return users

    @classmethod
    def get_all(cls):
        return cls.get_where("1")

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

def hostname_is_unique(hostname):
    if not isinstance(hostname, str):
        raise AttributeError
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()
    cur.execute("SELECT identifier FROM devices WHERE (hostname = %s OR altname = %s)",(hostname,hostname))
    results = cur.fetchall()
    if len(results) == 1:
        return True
    return False

