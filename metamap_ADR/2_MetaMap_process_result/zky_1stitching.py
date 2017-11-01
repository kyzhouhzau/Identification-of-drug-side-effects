#!/usr/bin/env python3

# -*- coding:utf-8 -*-
'''
author:Zhoukaiyin
$ python 2_MetaMap_process_result/Zky_1stitching.py [train_xml/test_xml]
we need stitch all of the test documents,because the metamap's websites only could process one text at one times. 
'''
import os
import sys
base = sys.argv[1]
path = r"1_remove_section"
path2 = r"2_MetaMap_process_result"
L = os.listdir(path+'/formatted_pro_'+base[:-4])
wf = open(path2 + '/Stitched_'+base[:-4]+'.txt', 'w')
for time in range(len(L)):
    rf = open(path + '/formatted_pro_'+base[:-4]+'/' + L[time], 'r')
    dom = rf.read()
    wf.write(dom+'\n')
    rf.close()
wf.close()
