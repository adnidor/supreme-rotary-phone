#!/usr/bin/python3
#coding=utf-8
import os,sys
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers



print("====== Geräte ======")
print("DO NOT EDIT - This file is generated automatically")

contexts = helpers.get_all_contexts()

for context in contexts:
    devices = helpers.get_devices_where("context = %s",(context.name,))
    print("====="+context.description+"=====")
    if len(devices) is 0:
        print("No devices in this context.")
        continue
    print("^Identifier ^IP ^Name ^Hostname ^Altname ^Typ ^Gerätetyp ^Verbindungstyp ^")
    for device in devices:
        altname = device.altname if device.altname else " "
        devicetype = device.devicetype_str if device.devicetype_str else " "
        print("|"+device.identifier+"|"+device.ip+"|"+device.description+"|"+device.hostname+"|"+altname+"|"+device.type+"|"+devicetype+"|"+device.connection+"|")


