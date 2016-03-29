#!/usr/bin/python3
import mysql.connector as ms
import sys
import ipaddress as ipa
import datetime

from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

now = datetime.datetime.now()


context = sys.argv[1] #erster Parameter

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT iprange FROM contexts WHERE name='"+sys.argv[1]+"'")
network = ipa.ip_network(cur.fetchone()[0])


DOMAIN=server_config.domain+"."
EMAIL=server_config.email
NS=server_config.nameserver

def print_header(suffix):
	print(";; "+suffix+" ("+context+")")
	print(";;DO NOT EDIT - File automatically generated from MySQL-Database." )
	print(";;")
	print("$TTL 0")
	print("@       IN      SOA     "+NS+". "+EMAIL.replace("@",".")+". (")
	print("                        "+now.strftime("%y%m%d%H%M")+"    ; Serial")
	print("                        3h              ; Refresh after 3 hours")
	print("                        1h              ; Retry after 1 hour")
	print("                        1w              ; Expire after 1 week")
	print("                        1h )            ; Negative caching TTL of 1 day")
	print("@       IN      NS      ns.intern.yannikenss.de.")

cur.execute("SELECT ip, hostname FROM devices WHERE context='"+context+"' ORDER BY INET_ATON(ip)")
if context == "root":
	prefix = ""
else:
	prefix = context+"."
print_header(str(network))
for row in cur.fetchall():
	ip = ipa.ip_address(row[0])
	last_digit = 0x000000ff & int(ip)
	hostname = row[1]
	fqhn = hostname+"."+prefix+DOMAIN
	print(str(last_digit)+" IN PTR "+fqhn)
