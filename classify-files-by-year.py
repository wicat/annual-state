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

def _move_pdf(src, dst):
    if os.path.exists(dst):
        print("DST<%s> EXISTS!" % dst)
    else:
        os.rename(src, dst)

def classify_2016():
    lls = []
    files = os.listdir("2016")
    for i in files:
        x = i.split(".")
        t = x[0][:6]

        u = x[0][6:]
        if "2016年年度报告" not in u:
            print(i)
        continue

        if t in lls:
            t = _rename_id(t, lls)
        lls.append(t)
        dst = TOPDIR + "2016/" + t + ".pdf"
        _move_pdf()

classify_2016()

