#!/bin/python2.7
# -*- coding: gbk -*-

## ��ע����ʦЭ����ҵ��Ϣ��ѯϵͳ��ץȡָ����ע����ʦ��Ϣ

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
        header = {"����":"",
                  "�Ա�":"",
                  "����ְ��":"",
                  "�Ƿ�Ա":"",
                  "ѧ��":"",
                  "ѧλ":"",
                  "��ѧרҵ":"",
                  "��ҵѧУ":"",
                  "�ʸ�ȡ�÷�ʽ������/���ˣ�":"",
                  "������׼�ĺ�":"",
                  "��׼ʱ��":"",
                  "ȫ�ƺϸ�֤���":"",
                  "ȫ�ƺϸ����":"",
                  "ע����ʦ֤����":"",
                  "�Ƿ�ϻ��ˣ��ɶ���":"",
                  "��׼ע���ļ���":"",
                  "��׼ע��ʱ��":"",
                  "����������":"",
                  "�����Ӧ���ѧʱ":"",
                  "����������ѧʱ":"",
                  "�ͽ估������Ϣ(��¶ʱ��:��2015������)":"",
                  "�μӹ���":"",
                  "��������":""}
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

        item += header["����"] + ","
        item += header["�Ա�"] + ","
        item += header["����ְ��"] + ","
        item += header["�Ƿ�Ա"] + ","
        item += header["��������"] + ","
        item += header["ѧ��"] + ","
        item += header["ѧλ"] + ","
        item += header["��ѧרҵ"] + ","
        item += header["��ҵѧУ"] + ","
        item += header["�ʸ�ȡ�÷�ʽ������/���ˣ�"] + ","
        item += header["������׼�ĺ�"] + ","
        item += header["��׼ʱ��"] + ","
        item += header["ȫ�ƺϸ�֤���"] + ","
        item += header["ȫ�ƺϸ����"] + ","
        item += header["ע����ʦ֤����"] + ","
        item += header["�Ƿ�ϻ��ˣ��ɶ���"] + ","
        item += header["��׼ע���ļ���"] + ","
        item += header["��׼ע��ʱ��"] + ","
        item += header["����������"] + ","
        item += header["�����Ӧ���ѧʱ"] + ","
        item += header["����������ѧʱ"] + ","
        item += header["�ͽ估������Ϣ(��¶ʱ��:��2015������)"] + ","
        item += header["�μӹ���"]

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
