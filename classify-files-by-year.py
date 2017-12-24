#!/bin/python2.7
# -*- coding: UTF-8 -*-  
import os

DIRS = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]
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

def _classify_1214(i, t, lls):
    if t in lls:
        t = _rename_id(t, lls)
    lls.append(t)
    dst = TOPDIR + "2010/" + t + ".pdf"
    _move_pdf("2012-2014/"+i, dst)
    return lls

def classify_1214():
    lls12 = []
    lls13 = []
    lls14 = []
    lls11 = []
    lls10 = []
    ost = []

'''
    files = []
    with open("2012-2014.txt", "rt") as f:
        for i in f:
            files.append(i.replace("\r", "").replace("\n", ""))
'''
    files = os.listdir("2012-2014")
    for i in files:
        x = i.split(".")
        t = x[0][:6]
        u = x[0][6:]

        if "10" in u:
            lls10 = _classify_1214(i, t, lls10)
        elif "11" in u:
            lls11 = _classify_1214(i, t, lls11)
        elif "12" in u:
            lls12 = _classify_1214(i, t, lls12)
        elif "13" in u:
            lls13 = _classify_1214(i, t, lls13)
        elif "14" in u:
            lls14 = _classify_1214(i, t, lls14)
        else:
            ost.append(i)
    print("ost=%d"%len(ost))

check_dir()
classify_1214()
