#!/usr/bin/python3
import ipaddress as ipa
import socket, struct
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import models
import helpers

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <ap>")
    exit(1)
ap = helpers.AccessPoint(sys.argv[1]) #erster Parameter

print("#DO NOT EDIT - This file was generated automatically from an MySQL-Database")

switchconfig = ap.switch.split(",") if ap.switch != "" else None

print("config interface 'loopback'")
print("    option ifname 'lo'")
print("    option proto 'static'")
print("    option ipaddr '127.0.0.1'")
print("    option netmask '255.0.0.0'")
print()

for vlan in ap.vlans:
    print("config interface 'vlan"+str(vlan.id)+"'")
    ifname= "option ifname '"
    for iface in ap.interfaces:
        ifname=ifname+iface+"."+str(vlan.id)+" "
    ifname=ifname.strip()+"'"
    print("    "+ifname)
    print("    option type 'bridge'")
    if vlan.id == ap.mvlan.id:
        print("    option proto 'dhcp'")
    else:
        print("    option proto 'none'")
        print("    option ipv6 0")
    print()

if switchconfig is not None:
    print("config switch")
    print("    option name 'switch0'")
    print("    option reset '1'")
    print("    option enable_vlan '1'")
    print()

    swvlans={}
    for port, swvlans_ctoan in enumerate(switchconfig):
        for vlan in swvlans_ctoan.split(" "):
            vlan_sani = vlan.strip("t")
            suffix = "" if not vlan.endswith("t") else "t"
            if vlan_sani in swvlans:
                swvlans[vlan_sani] = swvlans[vlan]+" "+str(port)+suffix
            else:
                swvlans[vlan_sani] = str(port)+suffix
                
    for vlan, ports in swvlans.items():
        print("config switch_vlan")
        print("    option device 'switch0'")
        print("    option vlan '"+vlan+"'")
        print("    option ports '"+ports+"'")
        print()


try:
    manual = open("/etc/networkmanagement/"+ap.name+".network.manual", "r")
    print(manual.read())
except IOError:
    pass
