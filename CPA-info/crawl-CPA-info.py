#!/bin/python2.7
# -*- coding: gbk -*-

## 从注册会计师协会行业信息查询系统上抓取指定的注册会计师信息

import urllib2, json, sys, urllib, requests, threading, time
from lxml import etree

class query_info_thread(threading.Thread):
    def __init__(self, guids, tid):
        self.guids = guids
        self.tid = tid
        threading.Thread.__init__(self)

    def query_info(self, guid, api2=False):
        flag = False
        item = str()
        header = {"姓名":"",
                  "性别":"",
                  "所内职务":"",
                  "是否党员":"",
                  "学历":"",
                  "学位":"",
                  "所学专业":"",
                  "毕业学校":"",
                  "资格取得方式（考试/考核）":"",
                  "考核批准文号":"",
                  "批准时间":"",
                  "全科合格证书号":"",
                  "全科合格年份":"",
                  "注册会计师证书编号":"",
                  "是否合伙人（股东）":"",
                  "批准注册文件号":"",
                  "批准注册时间":"",
                  "所在事务所":"",
                  "本年度应完成学时":"",
                  "本年度已完成学时":"",
                  "惩戒及处罚信息(披露时限:自2015年至今)":"",
                  "参加公益活动":"",
                  "出生日期":""}
        key = str()
        if api2:
            print "TRY AGAIN IN", guid
            url = "http://cmispub.cicpa.org.cn/cicpa2_web/003/%s.shtml" % guid
        else:
            url = "http://cmispub.cicpa.org.cn/cicpa2_web/07/%s.shtml" % guid

        html = urllib2.urlopen(url).read()
        page = etree.HTML(html)
        tds = page.xpath(u"//td")
        for td in tds:
            td = td.text
            if td != None:
                td = td.strip()
            if flag:
                header[key] = td
                flag = False
                continue
            if header.has_key(str(td)):
                key = str(td)
                flag = True

        item += header["姓名"] + ","
        item += header["性别"] + ","
        item += header["所内职务"] + ","
        item += header["是否党员"] + ","
        item += header["出生日期"] + ","
        item += header["学历"] + ","
        item += header["学位"] + ","
        item += header["所学专业"] + ","
        item += header["毕业学校"] + ","
        item += header["资格取得方式（考试/考核）"] + ","
        item += header["考核批准文号"] + ","
        item += header["批准时间"] + ","
        item += header["全科合格证书号"] + ","
        item += header["全科合格年份"] + ","
        item += header["注册会计师证书编号"] + ","
        item += header["是否合伙人（股东）"] + ","
        item += header["批准注册文件号"] + ","
        item += header["批准注册时间"] + ","
        item += header["所在事务所"] + ","
        item += header["本年度应完成学时"] + ","
        item += header["本年度已完成学时"] + ","
        item += header["惩戒及处罚信息(披露时限:自2015年至今)"] + ","
        item += header["参加公益活动"]

        if len(item) > 23:
            return item
        else:
            if not api2:
                return self.query_info(guid, True)
            return None

    def run(self):
        guids = self.guids
        cnt = self.tid
        items = list()
        for guid in guids:
            print guid
            try:
                item = self.query_info(guid)
                if item == None:
                    raise
                    continue
                items.append(item)
                print item
            except:
                with open("error-query-%d.csv" % cnt, "at") as ff:
                    ff.write(guid+'\n')
        with open("query-results-%d.csv" % cnt, "at") as f:
            for i in items:
                f.write(i+"\n")
        print "Completed!"


def query_name(name):
    guids = list()
    url = "http://cmispub.cicpa.org.cn/cicpa2_web/PersonIndexAction.do"
    paras = {"queryType":"2","perName":name,"isStock":"00","method":"indexQuery",
             "pageSize":"","pageNum":"","ascGuid":"","offName":"","perCode":""}
    req = requests.post(url, data=paras)
    html = req.text
    page = etree.HTML(html)
    hrefs = page.xpath(u"//a")
    for href in hrefs:
        try:
            d = dict(href.attrib)
            if d.has_key('href'):
                val = d['href']
                val = val.split("(")
                if len(val) < 2:
                    continue
                val = val[1].split(',')
                if val[0] < 10:
                    continue
                guids.append(val[0][1:-1])
        except:
            print "error in: %s" % href.attrib
    return guids

def name2guids():
    items = list()
    names = list()
    with open("names.csv", "rt") as f:
        for i in f:
            names.append(i.strip())
    for i in names:
        try:
            guids = query_name(i)
            if guids:
                items.extend(guids)
        except:
            with open("error-names.csv", "at") as ff:
                ff.write(i+'\n')
    with open("guids.csv", "at") as f:
        for i in items:
            f.write(i+"\n")
    print "Completed!"

def guids2info():
    guids = list()
    with open("guids.csv", "rt") as f:
        for i in f:
            guids.append(i.strip())
    gap = len(guids) / 10
    thrds = list()
    for i in range(9):
        thrd = query_info_thread(guids[gap*i:gap*(i+1)], i)
        thrds.append(thrd)
    thrds.append(query_info_thread(guids[gap*9:], 9))
    for thrd in thrds:
        thrd.setDaemon(True)
        thrd.start()
        time.sleep(1)
    for thrd in thrds:
        thrd.join()


guids2info()
