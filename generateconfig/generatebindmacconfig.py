#!/usr/bin/python3
import mysql.connector as ms
import sys,os
import datetime
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

now = datetime.datetime.now()

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


devices = helpers.get_devices_where("type = 'static' OR type = 'dhcp'")
print_header("mac."+DOMAIN)
for device in devices:
    print(device.identifier.replace(":",".")+" IN A "+device.ip)
    print(device.identifier.replace(":",".")+" IN TXT \""+device.fqdn+".\"")

