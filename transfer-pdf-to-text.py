#!/bin/python2.7
# -*- coding: UTF-8 -*-  

import os
from cStringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

def _move_pdf(src, dst):
    if os.path.exists(dst): print("DST<%s> EXISTS!" % dst)
    else: os.rename(src, dst)

def _list2str(l):
    s = str()
    for i in l: s += i.replace(",", r"，") + "|"
    return (s[:-1] if len(s) > 0 else "")

def parse_pdf(fname, outfile):
    
    pid = ""
    pyear = ""
    ptip = False
    ptip_text = ""
    ptip_type = 0
    ptip_cate = []
    ptip_iner = []
    ptip_outr = []
    padvise = False
    pone_page = False

    outfp = StringIO()
    fp = file(fname, 'rb')
    rsrcmgr = PDFResourceManager(caching=True)        
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").replace("\t","").strip()
        cells.append(cell)
        outfp.truncate(0)
        
    fp.close()
    device.close()
    outfp.close()
    
    with open(outfile, "at") as f:
        f.write(pid+",")
        f.write(pyear+",")
        ptip = "1" if ptip else "0"
        f.write(ptip+",")
        ptip_text = ptip_text.replace(",", r"，")
        f.write(ptip_text+",")
        f.write(str(ptip_type)+",")
        ptip_cate = _list2str(ptip_cate)
        f.write(ptip_cate+",")
        ptip_iner = _list2str(ptip_iner)
        f.write(ptip_iner+",")
        ptip_outr = _list2str(ptip_outr)
        f.write(ptip_outr+",")
        padvise = "1" if padvise else "0"
        f.write(padvise+",")
        pone_page = "1" if pone_page else "0"
        f.write(pone_page+"\n")    
    return

def wtf():
    files = os.listdir("stdata")
    cnt = 0
    for i in files:
        try:
            parse_pdf("stdata/"+i, "result.csv")
            _move_pdf("stdata/"+i, "stdata2/"+i)
        except:
            with open("error.log", "at") as f: f.write(i+"\n")
        cnt += 1
        if cnt % 100 == 0:
            print cnt
    print "Completed!"
    return


wtf()

