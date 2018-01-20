#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os, sys

reload(sys)
sys.setdefaultencoding("utf8")

def main():
    l_origin = list()
    l_later = list()
    with open("result-1516.csv", "rt") as f:
        for i in f:
            l_origin.append(i.replace("\n","").replace("\r",""))
    for i in l_origin:
        if i.split("\t") == 2:
            print i

    print "Completed!"
    return

main()
