#!/usr/bin/python3
#coding=utf-8
import sys
import helpers
from importlib.machinery import SourceFileLoader

server_config = SourceFileLoader("server_config", "/etc/networkmanagement/server_config.py").load_module()

targets = {
           "bind_dir":           {"value":server_config.bind_dir},
           "dokuwiki_dir":           {"value":server_config.dokuwiki_dir},
           "dnsmasq_config":           {"value":server_config.dnsmasq_config}
          }

if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" <target>")
    exit(1)
target = sys.argv[1] #erster Parameter

if target not in targets:
   print("unknown target")
   exit(1)

print(targets[target]["value"])
