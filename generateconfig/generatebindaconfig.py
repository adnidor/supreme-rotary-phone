#!/usr/bin/python3
import sys,os
import mysql.connector as ms
import datetime as dt
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers


if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <context>")
    exit(1)
context = helpers.Context(name=sys.argv[1]) #erster Parameter

DOMAIN=server_config.domain+"."
EMAIL=server_config.email
NS=server_config.nameserver

db = ms.connect(host=server_config.host,user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

def print_header(suffix):
    print(";; db."+suffix)
    print(";;DO NOT EDIT - File automatically generated from MySQL-Database. Edit "+suffix+"manual instead" )
    print(";;")
    print("$TTL 0")
    print("@       IN      SOA     "+NS+". "+EMAIL.replace("@",".")+". (")
    print("                        "+dt.datetime.now().strftime("%y%m%d%H%M")+"      ; Serial")
    print("                        3h              ; Refresh after 3 hours")
    print("                        1h              ; Retry after 1 hour")
    print("                        1w              ; Expire after 1 week")
    print("                        1h )            ; Negative caching TTL of 1 day")
    print("@       IN      NS      ns.intern.yannikenss.de.")

devices = context.get_devices()

if context.is_root():
    prefix = ""
else:
    prefix = context.name+"."

print_header(prefix+DOMAIN)
print()
print(";devices")
for device in devices:
    print(device.hostname+" IN A "+device.ip)
    print(device.hostname+" IN TXT \""+device.description+"\"")
    print(device.hostname+" IN TXT \""+device.identifier+"\"")
    if device.altname:
        print(device.altname+" IN CNAME "+device.hostname)

cur.execute("SELECT name, target FROM cnames WHERE context='"+context.name+"'")
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
