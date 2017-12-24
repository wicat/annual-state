#!/bin/python2.7
# -*- coding: UTF-8 -*-
import os

def _rename_id(id1, lls, c=1):
    id2 = "%s-%d" % (id1, c)
    if id2 in lls:
        _rename_id(id1, lls, c+1)
    return id2

def classify_2016():
    lls = []
    files = []
    with open("2016.txt", "rt") as f:
        for i in f:
            files.append(i.replace("\r", "").replace("\n", ""))
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

classify_2016()

