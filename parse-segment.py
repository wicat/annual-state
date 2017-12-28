#!/bin/python2.7
# -*- coding: UTF-8 -*-  

import os
from cStringIO import StringIO

DIRS = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]
TOPDIR = "stdata/"
RESDIR = "resdir"

RESULT = "result.txt"

def parse_pdf(fname, outfile, pdst):
    cnt = 1
    fid = fname.split("/")[-1].split(".")[0]
    outlist = list()
    outfp = StringIO()
    fp = file(fname, 'rb')
    
    rsrcmgr = PDFResourceManager(caching=True)        
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").rstrip()
        outfp.truncate(0)
        
        #outlist.append(cell)
        if r"重大风险提示" in cell:
            with open(outfile, "at") as f:
                f.write(fid+"\n")
                f.write("%d\n" % cnt)
                f.write(cell+"\n")
            if os.path.exists(pdst): print("DST <%s> EXISTS!" % pdst)
            else: os.rename(fname, pdst)

        if cnt == 10: break
        cnt += 1

    fp.close()
    device.close()
    outfp.close()
    return

def do_parse(fdate):
    psrc = "stdata/" + fdate
    pdst = "stdata2/" + fdate
    if not os.path.isdir(pdst): os.mkdir(pdst)

    files = os.listdir(psrc)
    for i in files:
        try:
            x = parse_pdf(psrc+i, "result.txt", pdst+i)
        except:
            with open("error.log", "at") as f:
                f.write(i+"\n")


retlist = [[],[],[],[],[]]
dirlist = [[],[],[],[],[]]
pdst = "stdata2/"

dirlist[0] = os.listdir(pdst + "2012")
dirlist[1] = os.listdir(pdst + "2013")
dirlist[2] = os.listdir(pdst + "2014")
dirlist[3] = os.listdir(pdst + "2015")
dirlist[4] = os.listdir(pdst + "2016")

with open(RESUTL, "rt") as f:
    x1 = ""
    x2 = ""
    x3 = ""
    cnt = 0
    pos = 0
    for i in f:
        if cnt == 3:
            cnt = 0
            if not dirlist[pos]:
                pos += 1
            

        if cnt == 0:
            x1 = i.replace("\n","").replace("\r","")+".pdf"
        elif cnt == 1:
            x2 = i.replace("\n","").replace("\r","")
        else:
            x3 = i.replace("\n","").replace("\r","")
        cnt += 1


