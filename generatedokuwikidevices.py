#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()



print("====== Geräte ======")
print("DO NOT EDIT - This file is generated automatically")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT name, description FROM contexts")

contexts = cur.fetchall()

for context in contexts:
	contextname = context[0]
	contextdesc = context[1]
	cur.execute("SELECT identifier, ip, description, hostname, altname, type FROM devices WHERE context='"+contextname+"' ORDER BY INET_ATON(ip)")
	print("====="+contextdesc+"=====")
	print("^Identifier ^IP ^Name ^Hostname ^Altname ^Typ ^")
	for row in cur.fetchall():
		mac = row[0]
		ip = row[1]
		description = row[2]
		hostname = row[3]
		altname = row[4] if row[4] else " "
		type = row[5]
		print("|"+mac+"|"+ip+"|"+description+"|"+hostname+"|"+altname+"|"+type+"|")


