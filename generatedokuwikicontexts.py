#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import server_config


print("====== Kontexte ======")
print("DO NOT EDIT - This file is generated automatically")
print("^Name ^IP-Range ^Beschreibung ^Link ^DHCP ^")

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

cur.execute("SELECT name,description,iprange,dhcp FROM contexts")

contexts = cur.fetchall()

for context in contexts:
	contextname  = context[0]
	contextdesc  = context[1]
	contextrange = context[2]
	contextdhcp = "Ja" if (context[3] == 1) else "Nein"
	print("|"+contextname+"|"+contextrange+"|"+contextdesc+"|[[network:devices_generated#"+contextdesc.lower()+"|Geräte]]|"+contextdhcp+"|")


