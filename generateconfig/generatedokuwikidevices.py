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

contexts = helpers.Context.get_all()

for context in contexts:
    devices = context.get_devices()
    print("====="+context.description+"=====")
    if len(devices) is 0:
        print("No devices in this context.")
        continue
    print("^Identifier ^IP ^Name ^Hostname ^Altname ^Typ ^Gerätetyp ^Verbindungstyp ^")
    for device in devices:
        altname = device.altname if device.altname else " "
        print("|"+device.identifier+"|"+device.ip+"|"+device.description+"|"+device.hostname+"|"+altname+"|"+device.type+"|"+device.devicetype.name+"|"+device.connection+"|")


