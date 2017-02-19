#!/usr/bin/python3
import subprocess
import sys,os
path = os.path.abspath(os.path.realpath(__file__)+"/../..")
sys.path.append(path)
sys.path.append("/etc/networkmanagement")
import server_config
import helpers

devices = helpers.Device.get_all()

for device in devices:
    if device.alwayson:
        print("object Host \""+device.fqdn+"\" {")
        print("  import \"generic-host\"")
        print("  display_name = \""+device.description+"\"")
        print("  address = \""+device.fqdn+"\"")
        print("  vars.context = \""+str(device.context.id)+"\"")
        print("  vars.os = \""+device.devicetype.os+"\"")
        if device.devicetype.os == "linux":
            print("  vars.distro = \""+device.osversion+"\"")
        awo = "true" if device.alwayson else "false"
        print("  vars.alwayson = "+awo)
        if device.formfactor != "":
            print("  vars.formfactor = \""+device.formfactor+"\"")
        if device.vmhost is not None:
            print("  parent_host_name = \""+device.vmhost.fqdn+"\"")
        print("}")
        print()
