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
wifidevice = {
     "type"     : "mac80211",
     "hwmode"   : "11g",
     "htmode"   : "HT20",
     "path"     : models.wireless_path[ap.model],
     "country"  : "DE",
     "channel"  : ap.channel,
     "disabled" : 0 if ap.wifi_enabled else 1
}
helpers.print_uci_dict(wifidevice, 4)
print()

wifis = helpers.WifiNetwork.get_all()

devices = helpers.Device.get_where("connection ='wifi'")


for wifi in wifis:
    if ap not in wifi.aps:
        continue
    print("config wifi-iface")
    wifi_iface = {
        "device"    : "radio0",
        "mode"      : wifi.mode,
        "ssid"      : wifi.ssid,
        "hidden"    : 1 if wifi.hidden else 0,
        "disabled"  : 0 if wifi.enabled else 0
    }
    if wifi.vlan is not None:
        wifi_iface.update({"network" : "vlan"+str(wifi.vlan.id)})
    if wifi.authmethod == 'none':
        wifi_iface.update({"encryption": "none"})
    elif wifi.authmethod == "radius":
        wifi_iface.update({"encryption" : "wpa2",
                           "auth_server": ap.radiusserver,
                           "auth_secret": ap.radiussecret})
    elif wifi.authmethod == "passphrase":
        wifi_iface.update({"encryption": "psk2",
                           "key"       : wifi.passphrase})
    elif wifi.authmethod == "wep":
        wifi_iface.update({"encryption": "wep",
                           "key"       : wifi.passphrase})
    if wifi.whitelist:
        mac_list = []
        for device in devices:
            if str(wifi.id) in device.ports:
                mac_list.append(device.identifier.strip())
        wifi_iface.update({"macfilter" : "allow",
                           "maclist"   : mac_list})
    if wifi.mode == "adhoc":
        wifi_iface.update({"bssid": wifi.bssid})
    helpers.print_uci_dict(wifi_iface, 4)
    print()
