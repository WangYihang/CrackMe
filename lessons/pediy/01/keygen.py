#!/usr/bin/env python
# encoding:utf-8

import sys

def get_key(username):
    data = [0x0C, 0x0A, 0x13, 0x09, 0x0C, 0x0B, 0x0A, 0x08]
    key = 0
    i = 3
    j = 0
    while True:
        if i >= len(username):
            break
        key += ord(username[i]) * data[j % 8]
        i += 1
        j += 1
    return key

def show_help():
    print "Usage : \n\tpython %s [username]" % sys.argv[0]

def main():
    if len(sys.argv) != 2:
        show_help()
        exit(1)
    print get_key(sys.argv[1])

if __name__ == "__main__":
    main()
