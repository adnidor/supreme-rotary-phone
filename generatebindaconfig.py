#!/usr/bin/python3
import mysql.connector as ms
import sys
import datetime
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

now = datetime.datetime.now()

context = sys.argv[1] #erster Parameter

db = ms.connect(host=server_config.host,user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

DOMAIN=server_config.domain+"."
EMAIL=server_config.email
NS=server_config.nameserver

def print_header(suffix):
	print(";; db."+suffix)
	print(";;DO NOT EDIT - File automatically generated from MySQL-Database. Edit "+suffix+"manual instead" )
	print(";;")
	print("$TTL 0")
	print("@       IN      SOA     "+NS+". "+EMAIL.replace("@",".")+". (")
	print("                        "+now.strftime("%y%m%d%H%M")+"      ; Serial")
	print("                        3h              ; Refresh after 3 hours")
	print("                        1h              ; Retry after 1 hour")
	print("                        1w              ; Expire after 1 week")
	print("                        1h )            ; Negative caching TTL of 1 day")
	print("@       IN      NS      ns.intern.yannikenss.de.")


cur.execute("SELECT ip, hostname, description, identifier, altname FROM devices WHERE context='"+context+"' ORDER BY INET_ATON(ip)")
if context == "root":
	prefix = ""
else:
	prefix = context+"."
print_header(prefix+DOMAIN)
print()
print(";devices")
for row in cur.fetchall():
	ip = row[0]
	hostname = row[1]
	description = row[2]
	identifier = row[3]
	altname = row[4]
	print(hostname+" IN A "+ip)
	print(hostname+" IN TXT \""+description+"\"")
	print(hostname+" IN TXT \""+identifier+"\"")
	if altname:
		print(altname+" IN CNAME "+hostname)

cur.execute("SELECT name, target FROM cnames WHERE context='"+context+"'")
print()
print(";cnames")
for row in cur.fetchall():
	name = row[0]
	target = row[1]
	print(name+" IN CNAME "+target)

print()
print(";manual")
try:
	manual = open("/etc/networkmanagement/"+prefix+DOMAIN+"manual", "r")
	print(manual.read())
except IOError:
	print()
