#!/usr/bin/python3
#coding=utf-8
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


print("Content-type: text/html; charset=UTF-8")
print()


print("<html><head>")
print("<title>Management</title>")
print("</head><body>")
print("<h1>Index</h1>")
print(str(helpers.get_secs_since_update())+" seconds since last update <a href=update.cgi>Update now</a>")
print("<br />")
print("<a href=list_devices.cgi>Geräteliste</a>")
print("<br />")
print("<a href=adddevice_form.cgi>Gerät hinzufügen</a>")
print("<br />")
print("<form action=search_device.cgi>")
print("<input type=text name=q /><input type=submit />")
print("</form>")
print("</body></html>")
