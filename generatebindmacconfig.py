#!/usr/bin/python3
import mysql.connector as ms
import sys
import datetime
import server_config

now = datetime.datetime.now()

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

DOMAIN="intern.yannikenss.de."

def print_header(suffix):
	print(";; db."+suffix)
	print(";;DO NOT EDIT - File automatically generated from MySQL-Database. Edit "+suffix+"manual instead" )
	print(";;")
	print("$TTL 0")
	print("@       IN      SOA     pi.yannik.intern.yannikenss.de. me.yannikenss.de. (")
	print("                        "+now.strftime("%y%m%d%H%M")+"      ; Serial")
	print("                        3h              ; Refresh after 3 hours")
	print("                        1h              ; Retry after 1 hour")
	print("                        1w              ; Expire after 1 week")
	print("                        1h )            ; Negative caching TTL of 1 day")
	print("@       IN      NS      ns.intern.yannikenss.de.")


cur.execute("SELECT identifier, ip, hostname FROM devices WHERE type='dhcp' OR type='static'")

print_header("mac."+DOMAIN)
for row in cur.fetchall():
	mac = row[0]
	ip = row[1]
	hostname = row[2]
	print(mac.replace(":",".")+" IN A "+ip)
	print(mac.replace(":",".")+" IN TXT \""+hostname+"\"")

