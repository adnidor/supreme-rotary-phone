#!/usr/bin/python3
#coding=utf-8
import os,sys
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers



print("====== Kontexte ======")
print("DO NOT EDIT - This file is generated automatically")
print("^Name ^IP-Range ^Beschreibung ^Link ^DHCP ^")

contexts = helpers.Context.get_all()

for context in contexts:
    dhcp = "Ja" if context.dhcp else "Nein"
    print("|"+context.name+"|"+context.iprange+"|"+context.description+"|[[network:devices_generated#"+context.description.lower()+"|Geräte]]|"+dhcp+"|")


