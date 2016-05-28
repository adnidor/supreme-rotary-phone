#!/usr/bin/python3
import mysql.connector as ms
import sys,os
import ipaddress as ipa
import datetime
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

now = datetime.datetime.now()

context = helpers.Context(name=sys.argv[1]) #erster Parameter
network = ipa.ip_network(context.iprange)

DOMAIN=server_config.domain+"."
EMAIL=server_config.email
NS=server_config.nameserver

def print_header(suffix):
    print(";; "+suffix+" ("+context.name+")")
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

devices = context.get_devices()
print_header(str(network))
for device in devices:
    ip = ipa.ip_address(device.ip)
    last_digit = 0x000000ff & int(ip)
    print(str(last_digit)+" IN PTR "+device.fqdn+".")
