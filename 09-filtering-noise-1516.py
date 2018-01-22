#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os, sys, logging
import jieba
from gensim import corpora, models, similarities

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#reload(sys)
#sys.setdefaultencoding("utf-8")

# return string
def _merge_after_remove_header_and_footer(l_pages):
    footerbet = u"1234567890-=+<>"
    l_segs = list()
    s_ret = str()
    nr_pages = len(l_pages)
    cnt = 0
    if nr_pages > 1:
        x1 = l_pages[0].replace(" ", "")
        x2 = l_pages[1].replace(" ", "")
        minlen = min(len(x1), len(x2))
        for i in range(minlen):
            if x1[i] != x2[i]:
                break
            cnt += 1
    ## remove header
    for i in l_pages:
        l_segs.append(i.replace(" ", "")[cnt:])
    ## remove footer and merge
    for i in l_segs:
        if len(i) == 0:
            continue
        while i[-1] in footerbet:
            i = i[:-1]
            if len(i) == 0:
                break
        s_ret += i
    return s_ret

def _split_by_tab_and_filte_english(l_origin):
    alphabet = u"QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
    l_later = list()
    for i in l_origin:
        tmp = i.replace(" ","")
        tmp_cnt = 0
        for j in tmp:
            if j in alphabet:
                tmp_cnt += 1
        if float(tmp_cnt) / len(tmp) > 0.1:
            continue
        l_later.append(i.split("\t"))
    return l_later

def _merge_and_split_by_keyword(l_origin):
    l_middle = list()
    l_later = list()
    for i in l_origin:
        if len(i) == 2:
            continue
        cnt = 0
        for j in i:
            if u"重要提示" in j or u"第一节" in j:
                if cnt < 8:
                    l_middle.append(i)
                break
            cnt += 1
    for i in l_middle:
        segment = _merge_after_remove_header_and_footer(i[2:])
        segments = segment.split(u"重要提示")
        if len(segments) == 2:
            l_later.append([i[0], i[1], segments[1]])
    return l_later

def _remove_duplicate(l_origin):
    lines = list()
    lines_list = list()
    for i in l_origin:
        tmp = i[2].split(u"。")
        lines.extend(tmp)
        lines_list.append(tmp)

    dictionaries = list()
    lsis = list()
    indexes = list()
    cnts =[0 for i in range(len(lines_list))]

    print "PRE"
    for item in lines_list:
        words = [[word for word in jieba.lcut(line)] for line in item]
        dictionary = corpora.Dictionary(words)
        corpus = [dictionary.doc2bow(word) for word in words]
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=20)
        index = similarities.MatrixSimilarity(lsi[corpus])
        dictionaries.append(dictionary)
        lsis.append(lsi)
        indexes.append(index)

    print "DO"
    for n in range(len(lines_list)):
        for line in lines_list[n]:
            compare_text = dictionaries[n].doc2bow(jieba.lcut(line))
            query_lsi = lsis[n][compare_text]
            sims = indexes[n][query_lsi]
            for key, val in enumerate(sims):
                if val > 0.99:
                    cnts[n] += 1
    print cnts
    print "DONE"

    '''
    for n in range(0, len(lines)):
        compare_text = dictionary.doc2bow(jieba.lcut(lines[n]))
        query_lsi = lsi[compare_text]
        sims = index[query_lsi]
        for m,elem in enumerate(sims):
            if elem >0.99:
                #print("{}&{}={}".format(len(lines[n]),len(lines[m]),elem))
                with open("res.txt", "at") as f:
                    f.write(lines[n]+"\n")
                break
    '''


def main():
    l_origin = list()
    l_later = list()
    with open("result-1516.csv", "rt") as f:
        for i in f:
            l_origin.append(unicode(i.replace("\n","").replace("\r",""), "utf-8"))
    print len(l_origin)
    l_later = _split_by_tab_and_filte_english(l_origin)
    print len(l_later)
    l_later = _merge_and_split_by_keyword(l_later)
    print len(l_later)
    _remove_duplicate(l_later)


    print "Completed!"
    return

if __name__ == '__main__':

    main()
