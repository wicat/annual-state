#!/bin/python2.7

import os

DIRS = ["2012", "2013", "2014", "2015", "2016"]
TOPDIR = "stdata/"
RESDIR = "resdir"

def _check_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def check_dir():
    for i in DIRS:
        _check_dir(TOPDIR+i)
    _check_dir(RESDIR)

def _rename_id(id1, lls, c=1):
    id2 = "%s-%d" % (id1, c)
    if id2 in lls:
        _rename_id(id1, lls, c+1)
    return id2

def classify_2016():
    lls = []
    llt = []
    files = os.listdir("2016")
    for i in files:
        x = i.split(".")
        t = x[0][6:]
        if t in lls:
            
        else:
            lls.append(t)

classify_2016()

