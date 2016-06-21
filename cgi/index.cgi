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

common_name = os.getenv("SSL_CLIENT_S_DN_CN")
auth = "Yes" if common_name is not None else "No"
authorized = "Yes" if helpers.is_user_authorized(common_name) else "No"

print("<html><head>")
print("<title>Management</title>")
print("</head><body>")
print("<h1>Index</h1>")
print("User: "+str(common_name)+", authenticated: "+auth+", authorized: "+authorized)
print("<br />")
secs_since_update = helpers.get_secs_since_update()
mins_since_update = int(secs_since_update / 60)
print(str(secs_since_update)+" seconds ("+str(mins_since_update)+" minutes) since last update <a href=update.cgi>Update now</a>")
print("<br />")
print("<br />")
print("<a href=list_devices.cgi>Geräteliste</a>")
print("<br />")
print("<a href=list_wifis.cgi>WLAN-Übersicht</a>")
print("<br />")
print("<a href=adddevice_form.cgi>Gerät hinzufügen</a>")
print("<br />")
print("<br />")
print("<form action=search_device.cgi>")
print("<input type=text name=q /><input type=submit value='Suchen'/>")
print("</form>")
if not os.path.exists("custom"):
    os.makedirs("custom")
cscripts = os.listdir("custom")
if len(cscripts) > 0:
    print("Custom Scripts:")
    print("<br />")
    for script in cscripts:
        if not script.startswith("."):
            print("<a href='custom/"+script+"'>"+script+"</a><br />")
print("</body></html>")
