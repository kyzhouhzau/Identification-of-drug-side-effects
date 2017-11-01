# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 21:30:42 2017

@author: jyy
@author:zhoukaiyin
we got the outputs of metamap ,then we use the following codes to separation those documents and give them their own true name 


"""
# 打开文件

import os
import sys
base = sys.argv[1]

path1 = r'2_MetaMap_process_result'
path3 = r'1_remove_section/formatted_pro_'+base[:-4]
file = open(path1+'/'+ base[:-4]+'.out', 'r')
# 文件标号
time = 0
line = file.readline()
# 写入文件
out_file = open(path1 + r'/metamapoutput_'+base[:-4]+'/' + str(time) + '.txt', 'w')
while line != '':
    # 匹配processing
    if len(line) < 10:
        out_file.write(line)
        line = file.readline()
    if line[0:10] == "Processing":
        # 文件标号-4位
        if int(line[11:15]) == time:
            out_file.write(line)
            line = file.readline()
        elif int(line[11:15]) == time + 1:
            time += 1
            out_file.close()
            out_file = open(path1 + r'/metamapoutput_'+base[:-4]+'/' + str(time) + '.txt', 'w')
            out_file.write(line)
            line = file.readline()
    else:
        out_file.write(line)
        line = file.readline()


'''
author zhoukaiyin
'''
L = os.listdir(path1+r'/metamapoutput_'+base[:-4]+'/')
L1 = os.listdir(path3)
for i in range(len(L)):
    key = L[i]
    value = L1[int(key[:-4])]
    oldName = os.path.join(path1+r'/metamapoutput_'+base[:-4]+'/', key)
    newName = os.path.join(path1+r'/metamapoutput_'+base[:-4]+'/', value)
    os.rename(oldName, newName)

