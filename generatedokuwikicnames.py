#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()



print("====== CNAMEs ======")
print("DO NOT EDIT - This file is generated automatically")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT name,description FROM contexts")

contexts = cur.fetchall()

for context in contexts:
	contextname  = context[0]
	contextdesc  = context[1]
	print("===== "+contextdesc+" =====")
	print("^Name ^Ziel ^")
	cur.execute("SELECT name,target FROM cnames WHERE context='"+contextname+"'")
	for cname in cur.fetchall():
		name = cname[0]
		target = cname[1]
		print("|"+name+"|"+target+"|")


