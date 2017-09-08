#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import socket, struct
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

DOMAIN = server_config.domain

db_connection = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)

class EqualityMixin:
    def __eq__(self, other):
        return (type(other) is type(self)) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class GetWhereMixin:
    @classmethod
    def get_where(cls, statement, vars=None):
        """Get Instance where the SQL statement matches

        :param str statement: SQL condition to be sent to server
        :param tuple vars: Variables for the SQL condition (optional)
        
        :returns: List of objects
        """
        cur = db_connection.cursor()
        sql = "SELECT " + cls._id_col + " FROM " + cls._table + " WHERE " + statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql, vars)
        results = cur.fetchall()
        objects = []
        for result in results:
            objects.append(cls(id=result[0]))
        return objects

    @classmethod
    def get_all(cls):
        """Like :func:`get_where` but doesn't take arguments, returns all entries instead"""
        return cls.get_where("1")


class Context(EqualityMixin, GetWhereMixin):
    """Gets a Context from the db

    :param str name: Context name, deprecated
    :param id: Context id
    """

    _table = "contexts"
    _id_col = "i"

    def __init__(self, name=None, id=None):
        if name is None and id is None:
            return
        if name is not None and isinstance(name, str):
            self.name = name
            cur = db_connection.cursor()
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
            self.id = int(id)
            cur = db_connection.cursor()
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
        return "<Context " + str(self.id) + ">"

    def __str__(self):
        return self.description

    def __eq__(self, other):
        return (self.id == other.id) and (self.name == other.name)

    def __hash__(self):
        return self.id

    def __len__(self):
        cur = db_connection.cursor()
        cur.execute("SELECT identifier FROM devices WHERE context = %s", (str(self.id),))
        result = cur.fetchall()
        return len(result)

    def get_devices(self, all_devices=None):
        """Get Devices in this Context

        If all_devices is supplied, don't query the database but use this list as the data source
        
        :param list all_devices: List of devices to search (optional)
        :returns: list of :class:`Device` objects
        """
        if all_devices is None:
            return Device.get_where("context = %s", (str(self.id),))
        else:
            return [d for d in all_devices if d.context == self]

    def is_root(self):
        """Check if Context is the root Context"""
        return self.parent is None

    def get_domain_part(self):
        if self.is_root():
            return ""
        else:
            return "." + self.name + self.parent.get_domain_part()

    def get_zonefile_name(self, suffix):
        if self.is_root():
            return "db.root." + suffix
        else:
            return "db" + self.get_domain_part() + "." + suffix

    @classmethod
    def get_root(cls):
        """Get root Context"""
        return cls.get_where("parent IS NULL")[0]

    def __contains__(self, other):
        if type(other) is Device:
            return other.context == self
        elif type(other) is str:
            result = Device.get_where("context = %s AND identifier = %s", (str(self.id), other,))
            return len(result) == 1


class Device(EqualityMixin, GetWhereMixin):
    """Get a Device from the db

    :param str identifier: The identifier of the device
    """

    _table = "devices"
    _id_col = "identifier"

    def __init__(self, identifier):
        if identifier is None:
            return
        self.identifier = identifier
        cur = db_connection.cursor()
        sql = """SELECT
                    devices.ip,
                    devices.context,
                    devices.hostname,
                    devices.altname,
                    devices.description,
                    devices.type,
                    devices.devicetype,
                    devices.connection,
                    devices.ports,
                    devices.internet,
                    devices.alwayson,
                    devices.formfactor,
                    devices.osversion,
                    devices.vmhost
                 FROM devices 
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
        self.devicetype = DeviceType(result[6])
        self.connection = result[7]
        self.ports = result[8].split(",") if self.connection == "wifi" else []
        self.port = result[8].split("/") if self.connection == "ethernet" else ['']
        self.portraw = result[8]
        self.internet = True if result[9] == 1 else False
        self.alwayson = True if result[10] == 1 else False
        self.formfactor = result[11]
        self.osversion = result[12]
        self.port_str = ""
        if self.ports == ['']:
            self.ports = []
        self.ports_str = []
        self.vmhost = None if not result[13] else Device(result[13])
        if self.connection == "wifi":
            for port in self.ports:
                cur.execute("SELECT ssid FROM wifis WHERE id=%s", (port,))
                self.ports_str.append(cur.fetchone()[0])
        elif self.connection == "ethernet" and self.port != ['']:
            sql = "SELECT description FROM switches WHERE id=%s"
            cur.execute(sql, (self.port[0],))
            result = cur.fetchone()[0]
            self.port_str = "Port %s auf %s" % (self.port[1], result)
        self.fqdn = self.get_fqdn()

    @classmethod
    def get_where(cls, statement, vars=None):
        """Get Instance where the SQL statement matches

        :param str statement: SQL condition to be sent to server
        :param tuple vars: Variables for the SQL condition (optional)
        
        :returns: List of objects
        """
        cur = db_connection.cursor()
        sql = "SELECT identifier FROM devices WHERE " + statement
        if vars is None:
            cur.execute(sql)
        else:
            cur.execute(sql, vars)
        results = cur.fetchall()
        devices = []
        for result in results:
            devices.append(cls(result[0]))
        return sorted(devices, key=Device.get_key)

    #use sparingly, really slow and resource intensive
    @classmethod
    def reliable_get_by_fqdn(cls, fqdn, all_devices):
        """Get a device by its FQDN (slow)
        
        :param str fqdn: The FQDN of the device
        :param list all_devices: List of devices to search (optional)

        :returns: Device object
        """
        if not isinstance(fqdn, str):
            raise TypeError

        if all_devices is None:
            all_devices = cls.get_all()
        for device in all_devices:
            if fqdn == device.get_fqdn() or fqdn == device.get_alt_fqdn():
                return device

        raise KeyError("Device not found")

    def __str__(self):
        return self.get_fqdn()

    def __repr__(self):
        return "<Device " + self.identifier + ">"

    def __eq__(self, other):
        return (self.identifier == other.identifier)

    def get_fqdn(self):
        """Get FQDN of the device"""
        return self.hostname + self.context.get_domain_part() + "." + DOMAIN

    def get_alt_fqdn(self):
        """Get FQDN of the device using the altname as a basis"""
        return self.altname + self.context.get_domain_part() + "." + DOMAIN

    def get_key(x):
        return struct.unpack("!I", socket.inet_aton(x.ip))[0]  #IP as number

    def write_to_db(self):
        """Write changes made to this object to the DB
        BETA!
        """
        db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
        cur = db.cursor()
        cur.execute("SELECT 1 FROM devices WHERE identifier = %s", (self.identifier,))
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


class WifiNetwork(EqualityMixin, GetWhereMixin):
    """Get a WifiNetwork from the db

    :param identifier int: The identifier of the network
    """
    _table = "wifis"
    _id_col = "id"

    def __init__(self, id):
        self.id = int(id)
        cur = db_connection.cursor()
        sql = """SELECT
                    ssid,
                    vlan,
                    authmethod,
                    aps,
                    hidden,
                    passphrase,
                    mode,
                    whitelist,
                    enabled,
                    bssid
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
        self.bssid = result[9]

    def __str__(self):
        return self.ssid

    def __repr__(self):
        return "<WifiNetwork " + str(self.id) + ">"


class Vlan(EqualityMixin, GetWhereMixin):
    """Get a Vlan from the db

    :param identifier int: The identifier of the vlan
    """
    _table = "vlans"
    _id_col = "id"

    def __init__(self, id):
        self.id = int(id)
        cur = db_connection.cursor()
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
        return "<Vlan " + str(self.id) + ">"


class DeviceType(EqualityMixin, GetWhereMixin):
    """Get a DeviceType from the db

    :param identifier int: The identifier of the devicetype
    """

    _table = "devicetypes"
    _id_col = "number"

    def __init__(self, id):
        self.id = int(id)
        cur = db_connection.cursor()
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

    def get_devices(self, all_devices=None):
        """Get Devices with ths DeviceType

        If all_devices is supplied, don't query the database but use this list as the data source
        
        :param list all_devices: List of devices to search (optional)
        :returns: list of :class:`Device` objects
        """
        if all_devices is None:
            return Device.get_where("devicetype = %s", (str(self.id),))
        else:
            return [d for d in all_devices if d.devicetype == self]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<DeviceType " + str(self.id) + ">"


class AccessPoint(EqualityMixin, GetWhereMixin):
    """Get a AccessPoint from the db

    :param identifier int: The identifier of the ap
    """

    _table = "aps"
    _id_col = "id"

    def __init__(self, id):
        self.id = int(id)
        cur = db_connection.cursor()
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
        return "<AccessPoint " + str(self.id) + ">"


def get_secs_since_update():
    """Get seconds since the last update was done.
    Reads `/etc/networkmanagement/last_update`

    :returns: int
    """
    file = open("/etc/networkmanagement/last_update")
    lastchange = int(file.readline())
    import time
    timestamp = int(time.time())
    return timestamp - lastchange


def is_user_authorized(cn):
    userfile = open("/etc/networkmanagement/authorized_users")
    for line in userfile:
        if cn in line:
            return True
    return False


def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text) - len(suffix)]


def get_device_from_fqdn(fqdn):
    """Tries to match a give FQDN to a Device. Works sometimes.
    If reliability is an issue, use :func:`Device.reliable_get_by_fqdn`

    :param str fqdn: FQDN"""
    if not fqdn.endswith(DOMAIN):
        return None
    hostcntxt = strip_end(fqdn, "." + DOMAIN)
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()
    contexts = Context.get_all()
    devcontext = None
    host = None
    for context in contexts:
        if hostcntxt.endswith(context.name):
            devcontext = context
            host = strip_end(hostcntxt, "." + devcontext.name)
            break
    if devcontext is None:
        devcontext = Context.get_root()
        host = strip_end(hostcntxt, ".")
    cur.execute("SELECT identifier FROM devices WHERE (hostname = %s OR altname = %s) AND context = %s", (host, host, devcontext.id))
    results = cur.fetchall()
    if len(results) != 1:
        return None
    return Device(results[0][0])


def hostname_is_unique(hostname):
    """Check if given hostname is unique

    :param str hostname: Hostname to be checked
    """
    if not isinstance(hostname, str):
        raise AttributeError
    db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
    cur = db.cursor()
    cur.execute("SELECT identifier FROM devices WHERE (hostname = %s OR altname = %s)", (hostname, hostname))
    results = cur.fetchall()
    if len(results) == 1:
        return True
    return False


def print_uci_dict(input_dict, indent=0):
    """Print a dictionary containing uci key-value pairs

    :param input_dict: Dictionary to print
    :param indent: Number of spaces used to indent the values
    """
    istring = " " * indent

    for key, value in input_dict.items():
        if type(value) is list:
            for item in value:
                print(istring + "list " + str(key) + " '" + str(item) + "'")
        elif value is None:
            continue
        else:
            print(istring + "option " + str(key) + " '" + str(value) + "'")
