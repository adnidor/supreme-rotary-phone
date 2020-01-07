#!/usr/bin/python3
import ipaddress as ipa
import socket, struct
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import helpers
import server_config

contexts = helpers.Context.get_all()
devices = {}
for context in contexts:
    devices[context] = context.get_devices()

needs_rules_dict = {}

for context in contexts:
    needs_rules = False
    last_internet = None
    for device in devices[context]:
        if last_internet is None:
            last_internet = device.internet
            continue
        if last_internet != device.internet:
            needs_rules = True
            break
        
    needs_rules_dict[context] = needs_rules

print("domain ip table filter chain SRPFILTER {")
for context in contexts:
    if len(context) == 0:
        continue
    action = f"goto SRP{context.id}" if needs_rules_dict[context] else "ACCEPT" if devices[context][0].internet else "REJECT"

    print(f"    saddr {context.iprange} {action} #{context.name}")
print("}")

for context in contexts:
    if len(context) == 0 or not needs_rules_dict[context]:
        continue
    print(f"domain ip table filter chain SRP{context.id} {{")
    print()
    print("    #"+context.description)

    for device in devices[context]:
        action = "ACCEPT" if device.internet else "REJECT"
        print(f"    saddr {device.ip} {action} #{device.fqdn}")

    print("}")


