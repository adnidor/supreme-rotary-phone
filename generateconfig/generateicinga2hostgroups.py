#!/usr/bin/python3
import subprocess
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers
import constants

contexts = helpers.Context.get_all()

for context in contexts:
    print("object HostGroup \"context-"+str(context.id)+"\" {")
    print("  display_name = \"Devices in "+context.description+"\"")
    print("  assign where host.vars.context == \""+str(context.id)+"\"")
    print("}")

for formfactor in constants.formfactors:
    print("object HostGroup \"formfactor-"+formfactor+"\" {")
    print("  display_name = \"Formfactor "+formfactor+"\"")
    print("  assign where host.vars.formfactor == \""+formfactor+"\"")
    print("}")
