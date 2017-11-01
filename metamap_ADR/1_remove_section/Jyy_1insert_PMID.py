#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
author:jyy
Enter $ metamap_test/1_remove_section [train_xml/test_xml]
This code help us insert PMID into text,which will help us process our text better. 
"""

import xml.dom.minidom
import os
import sys
base=sys.argv[1]
path = '1_remove_section'
L = os.listdir(path + '/'+base+'/')
for time in range(len(L)):
    dom = xml.dom.minidom.parse(path + '/'+base+'/' + L[time])
    txt = open(path + '/insert_PMID_'+base[:-4]+'/' + L[time][0:len([time]) - 4] + 'txt', 'w')
    root = dom.documentElement
    section = dom.getElementsByTagName('Section')
    for time_section in range(len(section)):
        # 获得第time_section个标签对之间的文本
        text = section[time_section].firstChild.data
        n = len(str(time))
        # for case in switch(n):
        if time < 10:
            v = '000' + str(time)

        elif 10 <= time < 100:
            v = '00' + str(time)

        elif 100 <= time < 1000:
            v = '0' + str(time)

        elif 1000 <= time < 10000:
            v = str(time)
        else:
            break
        txt.write('\n')
        txt.write('PMID- ' + v + '000' + str(time_section) + '\n')
        txt.write(text)
