#! usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import xml.dom.minidom
def extract(file,file_out):
    with open(file_out,'w') as wf:
        dom = xml.dom.minidom.parse(file)
        root = dom.documentElement
        mention = root.getElementsByTagName('Mention')
        for i,time_menction in enumerate(mention):
            m = time_menction
            st = m.getAttribute("str").lower()
            start = m.getAttribute("start")
            wf.write(str([start,[st]])+'\n')

def main():
    path1 = '3_standardization/result_train/'
    path2 = '4_evaluation/prediction_train/'
    path3 = '1_remove_section/train_xml_for_evaluation/'
    path4 = '4_evaluation/true_train/'
    L = os.listdir(path1)
    for i, time in enumerate(L):
        extract(path1+time,path2+time[:-4]+'.txt')
    L1 = os.listdir(path3)[:39]
    for i, time in enumerate(L1):
        extract(path3+time,path4+time[:-4]+'.txt')

if __name__ == '__main__':
    main()
