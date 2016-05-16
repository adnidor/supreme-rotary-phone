#!/usr/bin/python3
import mysql.connector as ms
import ipaddress as ipa
import socket, struct
import sys,os
from subprocess import check_output,call
import syslog
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

syslog.openlog("wifi-cert-check")

if len(sys.argv) != 5:
    print("usage: "+sys.argv[0]+" <ca-file> <cert-file> <client-ip> <supplicant-mac>")
    exit(1)
cafile = sys.argv[1]
certfile = sys.argv[2]
clientip = sys.argv[3]
supplicantmac = sys.argv[4]

cn_opensslcommand = "openssl x509 -noout -subject -in '%s' | sed -n '/^subject/s/^.*CN=//p'"%(certfile,)
verify_opensslcommand = "openssl verify -CApath '%s' '%s'"%(cafile,certfile)

common_name = check_output(cn_opensslcommand,shell=True,universal_newlines=True).strip()
syslog.syslog("CN: "+common_name)

db = ms.connect(host=server_config.host, user=server_config.user, passwd=server_config.passwd, db=server_config.db)
cur = db.cursor()

identifier = helpers.get_identifier_from_fqdn(common_name)
if identifier is None:
    print("Device not found")
    syslog.syslog("Device not found")
    exit(1)

cur.execute("SELECT ip FROM devices WHERE connection='wifi' AND identifier=%s", (identifier,))
results = cur.fetchall()
if len(results) == 0:
    print("Device not authorized")
    syslog.syslog("Device not authorized")
    exit(1)
elif len(results) > 1:
    print("multiple results found, aborting")
    syslog.syslog("multiple devices found")
    exit(1)
syslog.syslog("IP: "+results[0][0])

try:
    exit(call(verify_opensslcommand,shell=True))
except Exception as test:
    syslog.syslog("Fehler mit openssl: "+test.output)
    exit(1)
