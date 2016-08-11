#!/usr/bin/python3
#coding=utf-8
import mysql.connector as ms
import sys
import helpers

if len(sys.argv) != 3:
    print("usage: "+sys.argv[0]+" <contextid> <suffix>")
    exit(1)
contextid = sys.argv[1] #erster Parameter
suffix = sys.argv[2]

context = helpers.Context(id=contextid)
print(context.get_zonefile_name(suffix))
