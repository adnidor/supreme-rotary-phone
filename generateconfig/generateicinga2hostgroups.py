#!/usr/bin/python3
import subprocess
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

contexts = helpers.Context.get_all()

for context in contexts:
    print("object HostGroup \"context-"+str(context.id)+"\" {")
    print("  display_name = \"Devices in "+context.description+"\"")
    print("  assign where host.vars.context == \""+str(context.id)+"\"")
    print("}")
