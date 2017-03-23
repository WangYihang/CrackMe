#!/usr/bin/env python
# encoding:utf-8

import sys

def check_password(username, password):
    v2 = 0
    for i in password:
        v7 = v2
        v3 = 0
        if (ord("0") < ord(i)) and (ord("9") > ord(i)):
            v3 = 1
        v5 = v7
        if v3 == 1:
            break
        v5 = ord(i) - 48
        v2 = 10 * v5
    print v5


def get_password(username):
    password = ""
    print password

def show_help():
    print "Usage : \n\tpython %s [username]" % sys.argv[0]

def main():
    # if len(sys.argv) != 2:
    #     show_help()
    #     exit(1)
    # get_password(sys.argv[1])
    check_password("admin", "password")

if __name__ == "__main__":
    main()
