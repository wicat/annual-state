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

DIRS = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]
TOPDIR = "stdata/"
RESDIR = "resdir"

def parse_pdf(fname, outfile):
    cnt = 1
    outlist = list()
    outfp = StringIO()
    rsrcmgr = PDFResourceManager(caching=True)        
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    
    fp = file(fname, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        outlist.append(outfp.getvalue().replace("\n","").replace("\r",""))

        if cnt == 10: break
        cnt += 1

    fp.close()
    device.close()
    outfp.close()
    return outlist


x = parse_pdf("test.pdf", "a.txt")
for i in x:
    print i
