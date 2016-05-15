#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
import ipaddress
import re
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers
import cgi
import cgitb
cgitb.enable()

ipregex = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
macregex = re.compile("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$")

print("Content-type: text/html; charset=UTF-8")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

if "q" not in cgi.FieldStorage():
    print("Kein Gerät angegeben")
    exit(1)
q = cgi.FieldStorage().getfirst("q")

if ipregex.match(q):
    cur.execute("SELECT identifier FROM devices WHERE ip = %s", (q,))
    results = cur.fetchall()
    if len(results) == 0:
        print()
        print("no devices found (ip)")
        exit(1)
    device = results[0][0]
elif macregex.match(q.lower()):
    cur.execute("SELECT identifier FROM devices WHERE identifier = %s", (q.replace("-",":"),))
    results = cur.fetchall()
    if len(results) == 0:
        print()
        print("no devices found (mac)")
        exit(1)
    device = results[0][0]
else:
    print()
    print("unknown format")
    exit(1)

print("Location: show_device.cgi?device="+device)
