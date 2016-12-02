#!/usr/bin/python3
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
config_file = os.getenv("config")
port = os.path.basename(config_file)
syslog.syslog("CN: "+str(common_name))
syslog.syslog("Config: "+str(config_file))
syslog.syslog("Port: "+str(port))

results = helpers.Device.get_where("connection='openvpn' AND identifier=%s", (common_name,))
if len(results) == 0:
    print("CN not found")
    syslog.syslog("CN not found")
    exit(1)
elif len(results) > 1:
    print("multiple results found, aborting")
    syslog.syslog("multiple devices found")
    exit(1)

if port not in results[0].portraw.split(","):
    syslog.syslog("wrong network")
    exit(1)
syslog.syslog("IP: "+results[0].ip)
tmp_file.write("ifconfig-push "+results[0].ip+" 255.255.255.0\n")
if results[0].internet:
    tmp_file.write("push \"redirect-gateway def1\"\n")
tmp_file.close()

try:
    exit(call(["/etc/openvpn/proxyarp-connect.sh", results[0].ip]))
except FileNotFoundError:
    pass
