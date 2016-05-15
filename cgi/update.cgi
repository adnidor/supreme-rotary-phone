#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
import ipaddress
import subprocess as sp
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers
import cgi
import cgitb
cgitb.enable()

print("Content-type: text/html")
print()

result = sp.call(["sudo",path+"/update.sh"])
if result == 0:
    print("Update successful")
else:
    print("Update failed with code "+str(result))
print("<a href=..>Home</a>")
