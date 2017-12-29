#!/bin/python2.7
# -*- coding: UTF-8 -*-  

import os
from cStringIO import StringIO

DIRS = ["2012", "2013", "2014", "2015", "2016"]

def load_data(path):
    data = []
    asid = str()
    line = str()
    text = str()
    cnt = 1
    with open(path, "rt") as f:
        for i in f:
            if cnt == 1:
                asid = i.strip()
            elif cnt == 2:
                line = i.strip()
            else:
                text = i.strip()
                data.append([asid, line, text])
                cnt = 0
            cnt += 1
    return data


def parse_data(path):
    data = load_data(path)
    for cell in data:
        x = cell[2].replace(" ","").find(r"重大风险提示")
        if x > 100 and x < 150:
            print cell[0]
            print cell[2]


parse_data("result-2012.txt")
