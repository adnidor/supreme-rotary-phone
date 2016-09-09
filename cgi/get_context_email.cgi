#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
import ipaddress
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers
import cgi
import cgitb
cgitb.enable()

submitted = cgi.FieldStorage()

print("Content-type: text/plain")
print()


if not "context" in submitted:
    print("Es fehlen Eingaben")
    exit(1)

context = helpers.Context(id=submitted.getfirst("context"))
print(context.email)
