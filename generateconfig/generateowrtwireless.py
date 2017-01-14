#!/usr/bin/python3
import sys, os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import models
import helpers

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <apid>")
    exit(1)
ap = helpers.AccessPoint(sys.argv[1]) #erster Parameter

print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

print("config wifi-device 'radio0'")
print("    option type 'mac80211'")
print("    option hwmode '11g'")
print("    option htmode 'HT40'")
print("    option path '"+models.wireless_path[ap.model]+"'")
print("    option country 'DE'")
print("    option channel '"+str(ap.channel)+"'")
if not ap.wifi_enabled:
    print("    option disabled '1'")
print()

wifis = helpers.WifiNetwork.get_all()

devices = helpers.Device.get_where("connection ='wifi'")


for wifi in wifis:
    if ap not in wifi.aps:
        continue
    print("config wifi-iface")
    print("    option device 'radio0'")
    print("    option mode '"+wifi.mode+"'")
    print("    option ssid '"+wifi.ssid+"'")
    if wifi.hidden:
        print("    option hidden '1'")
    if wifi.vlan is not None:
        print("    option network 'vlan"+str(wifi.vlan.id)+"'")
    if wifi.authmethod == 'none':
        print("    option encryption 'none'")
    elif wifi.authmethod == "radius":
        print("    option encryption 'wpa2'")
        print("    option auth_server '"+ap.radiusserver+"'")
        print("    option auth_secret '"+ap.radiussecret+"'")
    elif wifi.authmethod == "passphrase":
        print("    option encryption 'psk2'")
        print("    option key '"+wifi.passphrase+"'")
    elif wifi.authmethod == "wep":
        print("    option encryption 'wep'")
        print("    option key '"+wifi.passphrase+"'")
    if wifi.whitelist:
        for device in devices:
            if str(wifi.id) in device.ports:
                print("    list maclist '"+device.identifier.strip()+"'")
        print("    option macfilter 'allow'")
    if not wifi.enabled:
        print("    option disabled '1'")
    else:
        print("    option disabled '0'")
    if wifi.mode == "adhoc":
        print("    option bssid '"+wifi.bssid+"'")
    print()
