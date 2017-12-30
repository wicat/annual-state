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

def parse_pdf(fname, outfile):
    outfp = StringIO()
    fp = file(fname, 'rb')
    cells = []
    
    rsrcmgr = PDFResourceManager(caching=True)        
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").replace("\t","").strip()
        cells.append(cell)
        outfp.truncate(0)
        
    with open(outfile, "at") as f:
        for cell in cells:
            f.write(cell+"\n")

    fp.close()
    device.close()
    outfp.close()
    return


def wtf():
    files = os.listdir("stdata")
    cnt = 0
    for i in files:
        try:
            parse_pdf("stdata/"+i, "stdata2/%s.txt"% (i.split(".")[0]))
        except:
            with open("error.log", "at") as f: f.write(i+"\n")
        cnt += 1
        if cnt % 100 == 0:
            print cnt
    print "Completed!"
    return


wtf()

