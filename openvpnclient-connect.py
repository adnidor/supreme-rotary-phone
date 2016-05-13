#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
from subprocess import call
import syslog
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

syslog.openlog("openvpnclient-connect")

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <tmpfile>")
    exit(1)
tmp_filepath = sys.argv[1]
tmp_file = open(tmp_filepath, "w")
syslog.syslog("tmp_file: "+tmp_filepath)

common_name = os.getenv("common_name")
syslog.syslog("CN: "+common_name)

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT ip FROM devices WHERE type='vpn' AND identifier=%s", (common_name,))
results = cur.fetchall()
if len(results) == 0:
    print("CN not found")
    syslog.syslog("CN not found")
    exit(1)
elif len(results) > 1:
    print("multiple results found, aborting")
    syslog.syslog("multiple devices found")
    exit(1)
syslog.syslog("IP: "+results[0][0])
tmp_file.write("ifconfig-push "+results[0][0]+" 255.255.255.0\n")
tmp_file.close()

try:
    exit(call("/etc/openvpn/proxyarp-connect.sh"))
except FileNotFoundError:
    pass
