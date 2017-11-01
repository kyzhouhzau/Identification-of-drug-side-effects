# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 09:37:38 2017

@author: jyy
$python 1_remove_section/Jyy_2formatted_pro.py [train_xml/test_xml]
we known that metamap need formatted text ,so we use this code to replace some large space by ';',that can help us impove its processing efficiency. 
"""
import os
import re
import sys
base=sys.argv[1]

def init(line):
    line = re.sub(r"    \s+", ";", line)
    if (line == "\n"):
        line = " \n"
    return line


# 文件读写路径
path = r"1_remove_section"
# 文件列表
L = os.listdir(path + '/insert_PMID_'+base[:-4]+'/' )
# 处理每一个文件
for file_name in L:
# 输入
    text = open(path + '/insert_PMID_'+base[:-4]+'/' + file_name, 'r')
# 输出
    out_file = open(path + '/formatted_pro_' + base[:-4]+'/'+file_name, 'w')

    line = init(text.readline())
    while line != '':
# 识别PMID
        if line[0:5] == "PMID-":
            out_file.write("\n")
            out_file.write(line)
            line = init(text.readline())
            if re.search(r"^\s+\n", line) == None:
                out_file.write("TI -" + line)
            else:
                while re.search(r"^\s+\n", line) != None:
                    line = init(text.readline())
                out_file.write("TI -" + line)
            line = init(text.readline())
            if re.search(r"^\s+\n", line) == None:
                out_file.write("AB -" + line)
            else:
                while re.search(r"^\s+\n", line) != None:
                    line = init(text.readline())
                out_file.write("AB -" + line)
            line = init(text.readline())
        if re.search(r"^\s+\n", line) != None:
            line = init(text.readline())
        else:
            out_file.write(line)
            line = init(text.readline())
    out_file.close()
