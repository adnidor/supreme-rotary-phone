#!/usr/bin/python3
import subprocess
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

users = helpers.User.get_all()

for user in users:
    print("object User \""+user.username+"\" {")
    print("  import \"generic-user\"")
    print("  display_name = \""+user.name+"\"")
    print("  email = \""+user.email+"\"")
    if user.pushover is not None:
        print("  vars.pushover_key = \""+user.pushover+"\"")
