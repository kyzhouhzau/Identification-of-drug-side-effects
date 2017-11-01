#! usr/bin/env python3
# -*- coding:utf-8 -*-

'''


Author:Zhoukaiyin
open your terminal in work dir
$ python 3_MetaMap_process_result/zhy_phase_compare.py [train_xml/test_xml]
with the outputs of metamap we should do some extraction ,firstly we try extract the first candidates which has the higherest score,then we extract entities that we intreasted by 
their attribute tags finally we write all those results into our result documents accompanied by their start locations ,lens and tags.


'''

import re
import os
import xml.dom.minidom
import sys
base=sys.argv[1]
from  Levenshtein import  StringMatcher
#提取MetaMap处理结果获得评分最高的'Meta Candidates'
#对抽取的第一条结果按照【Anatomical Abnormality】内的标签进行抽取
def get_source(file_,file,outfile):
    with open(file,'r') as f:
        lines = f.readlines()
    with open(outfile, 'w') as wf:
        s = get_section(file_)
        len = s[1]
        for i,line in enumerate(lines):
            if str(line[11:19]).isdigit():
                wf.write(line.lower()+'\n')

            if 'Phrase:' in line:
                wf.write(line.lower())
            if 'Meta Candidates' in line:
                line = lines[i+1]
                set = (
                    'Anatomical Abnormality', 'Cell or Molecular Dysfunction', 'Congenital Abnormality',
                    'Disease or Syndrome',
                    'Experimental Model of Disease', 'Injury or Poisoning', 'Mental or Behavioral Dysfunction',
                    'Neoplastic Process ', 'Pathologic Function', 'Sign or Symptom', 'Organism Function'
                      )
                index_start = line.find('[')
                index_end = line.find(']')
                tag = line[index_start + 1:index_end]
                if tag in set:
                    if line.find('Adverse reactions') == -1 and line.find('see') == -1:
                        wf.write(line.lower().strip()+'\n')

        wf.write('processing 0000000' + str(len))
#对抽取到的句子以及高评分的'Meta Candidates'进行格式化并放入字典

def re_write(file,file2):
    with open(file,'r') as rf:
        lines = rf.readlines()
    with open (file2,'w') as wf:
        for i, line in enumerate(lines):
            if line[15:19] == '0001':
                wf.write('processing 00000000'+'\n')
                wf.write(line)
            elif line[15:19] == '0002':
                wf.write('processing 00000001'+'\n')
                wf.write(line)
            elif line[15:19] == '0003':
                wf.write('processing 00000002'+'\n')
                wf.write(line)
            else:
                wf.write(line)



def filter_source(file,n=0):
    with open(file,'r') as rf:

            lines = rf.readlines()
            l = []
            k = []
            for i, line in enumerate(lines):
                if line[15:19] == '000'+str(n):
                    l.append(i)
                if line[15:19] == '000'+str(n+1) :
                    k.append(i)
            tag1 = l[0]
            tag2 = k[0]

            names = lines[tag1:tag2]
            for h,name in enumerate(names):
                if str(name[:2]).isdigit():
                    yield {
                                    'Pahse': names[h - 1][8:].replace(';', '').strip('\n').strip(),
                                    'Word': name.strip('\n').strip()
                            }
#将字典中的phase定位到字典中并寻找起始实位置，再将word即要标出的副作用定位到句子中计算两者索引之和得到最终索引值。
#由于我们获得的句子是如下格式？  1000   TO (Togo) [Geographic Area]？这样的话括号中的词就要求与前面的词进行比
# 对区重，以及与句子进行比对去除高得分的，最终获得需要的
def phase_compare(docu,file,n):
        dom = docu.lower()
        drs = filter_source(file,n)
        for i,e in enumerate(drs):
            try:
                lis = []
                word = e['Word']
                phase_=e['Pahse']
                index = dom.find(str(phase_))
                # print(e['Pahse'])
                # print(index)
                # print('\n')
                if index !=-1:
                    patten = re.compile('\d*')
                    result = re.search(patten,word)
                    index_begin = word.index(str(result.group()))
                    index_middle = word.find('(')
                    index_end = word.find(')')
                    index_last = word.find('[')
                    if len(result.group()) > 3:
                        if ')' in word:
                            tag1 = word[index_begin+4:index_middle]
                            tag2 = word[index_middle+1:index_end]
                            lis.append(tag1.strip())
                            lis.append(tag2.strip())
                        else:
                            tag3 = word[index_begin+4:index_last]
                            lis.append(tag3.strip())
                    else:
                        if ')' in word:
                            tag1 = word[index_begin+4:index_middle]
                            tag2 = word[index_middle+1:index_end]
                            lis.append(tag1.strip())
                            lis.append(tag2.strip())
                        else:
                            tag3 = word[index_begin+4:index_last]
                            lis.append(tag3.strip())
                    #去重
                    aim_word = set(lis)
                    aim_word_ = list(aim_word)
                    #比对
                    if len(aim_word_)==2:
                        s1 = aim_word_[0]
                        s2 = aim_word_[1]
                        len1 = StringMatcher.ratio(s1, phase_)
                        len2 = StringMatcher.ratio(s2, phase_)
                        aim_word_.clear()
                        if len1>len2:
                            aim_word_.append(s1)
                        else:
                            aim_word_.append(s2)
                    if len(aim_word_) == 1:
                        s3 = aim_word_[0]
                        aim_word_.clear()
                        aim_word_.append(s3)
                    index1 = phase_.find(aim_word_[0].strip())
                    if index1!=-1:
                        global index2
                        index2 = index+index1
                        yield {
                                'index': index2,
                                'word': aim_word_[0],
                                'len': len(aim_word_[0])
                                }
                        X = 'a'*len(aim_word_[0])
                        word = dom[index2:index2+len(aim_word_[0])]
                        dom = dom.replace(word,X,1)
            except KeyError:
                continue

def get_section(file,n=0):
    dom = xml.dom.minidom.parse(file)
    section = dom.getElementsByTagName('Section')
    l = len(section)
    dom = section[n].firstChild.data
    return [dom,l]

def sec_write(file,file_,file_out):
    #file是最初的无标签文件.xml，file_经过提取过滤的文件.txt,file_out结果文件.xml
    with open(file,'r') as rf:
        lines = rf.readlines()
    with open(file_out, 'w') as wf:
            s = get_section(file)
            for i,line in enumerate(lines):
                if 'Mentions' not in line:
                    wf.write(line)
                else:
                    wf.write('  <Mentions>' + '\n')
                    k = 1
                    for n in range(0, s[1]):
                        ww =phase_compare(get_section(file,n)[0],file_,n)
                        if ww:
                            for l,w in enumerate(ww):
                                start = w['index']
                                word = w['word']


                                len = w['len']
                                line_next = '    '+'<Mention id="M'+str(k)+'" section="S'+str(n+1)+'" type="AdverseReaction" start="' \
                                                            + str(start) +  '" len="' + str(len) + '" str="'+ word+'"/>'
                                wf.write(line_next+'\n')
                                k+=1
                    wf.write('  </Mentions>' + '\n')

def write_to_mentions(file,file_,file_out):
    s = get_section(file)
    if s[1]==1:
        sec_write(file,file_,file_out)
    elif s[1]==2:
        sec_write(file, file_, file_out)
    elif s[1]==3:
        sec_write(file, file_, file_out)

def main():
    path1 = '2_MetaMap_process_result/metamapoutput_'+base[:-4]+'/'
    path2 = '3_standardization/metamapout_'+base[:-4]+'/'
    path3 = '1_remove_section/'+base+'/'
    path4 = '3_standardization/result_'+base[:-4]+'/'
    path5 = '3_standardization/2metamapout_'+base[:-4]+'/'
    L = os.listdir(path1)
    for i,time in enumerate(L):
        get_source(path3+time[:-4]+'.xml',path1+time,path2+time)
        re_write(path2+time, path5+time)
        filter_source(path2+time)
        write_to_mentions(path3+time[:-4]+'.xml',path5+time[:-4]+'.txt',path4+time[:-4]+'.xml')

if __name__ == '__main__':
    main()
