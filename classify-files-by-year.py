#!/bin/python2.7
# -*- coding: UTF-8 -*-  
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
        id2 = _rename_id(id1, lls, c+1)
    return id2

def _move_pdf(src, dst):
    if os.path.exists(dst):
        print("DST<%s> EXISTS!" % dst)
    else:
        os.rename(src, dst)

def classify_1516():
    lls = []
    files = os.listdir("2015")
    for i in files:
        x = i.split(".")
        t = x[0][:6]

        if t in lls:
            t = _rename_id(t, lls)
        lls.append(t)
        dst = TOPDIR + "2015/" + t + ".pdf"
        _move_pdf("2015/"+i, dst)

classify_1516()
