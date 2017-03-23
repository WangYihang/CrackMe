#!/usr/bin/env python
# encoding:utf-8

import sys

def get_password(username):
    password = 0
    i = 0
    j = 45
    while True:
        if i >= len(username):
            break
        password += j * ord(username[i])
        i += 1
        j += 1
    print "Username : [ %s ]\nPassword : [ %s ]" % (username, password)

def show_help():
    print "Usage : \n\tpython %s [username]" % sys.argv[0]

def main():
    if len(sys.argv) != 2:
        show_help()
        exit(1)
    get_password(sys.argv[1])

if __name__ == "__main__":
    main()
