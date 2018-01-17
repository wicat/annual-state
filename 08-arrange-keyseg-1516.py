#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os, traceback, sys, chardet
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

reload(sys)
sys.setdefaultencoding("utf8")

def _move_pdf(src, dst):
    if os.path.exists(dst): print("DST<%s> EXISTS!" % dst)
    else: os.rename(src, dst)

def parse_pdf(fname, outfile):
    _pid = fname.split("/")[-1].split(".")[0].split("+")
    pid = _pid[1]
    pyear = _pid[0]
    cnt = 0
    cells = list()

    outfp = StringIO()
    fp = file(fname, 'rb')
    rsrcmgr = PDFResourceManager(caching=True)
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").replace("\t","")[:-1]
        outfp.truncate(0)

        ###------------------------------------###
        cnt += 1
        tmpcell = cell.replace(" ","")
        if cnt > 10 or r"目录" in tmpcell: break
        cells.append(cell)
        ###------------------------------------###

    cellstr = pyear + "\t" + pid + "\t"
    for i in cells:
        cellstr += i + "\t"
    cellstr = cellstr[:-1] + "\n"
    with open(outfile, "at") as f:
        f.write(cellstr)

    fp.close()
    device.close()
    outfp.close()
    return

def main():
    files = os.listdir("stdata-1516")
    for i in files:
        try:
            parse_pdf("stdata-1516/"+i, "result-1516.csv")
            _move_pdf("stdata-1516/"+i, "stdata-1516-success/"+i)
        except:
            with open("error.log", "at") as f: f.write(i+"\n")
    print "Completed!"
    return


