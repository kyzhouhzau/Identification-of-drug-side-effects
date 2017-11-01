#! usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import csv

def compare(file1,file2,filename):

    with open(file1,'r') as rf:
        lines1 = rf.readlines()
    with open(file2, 'r') as f:
        lines2 = f.readlines()
        i = 0
        for n,line1 in enumerate(lines1):
            for k,line2 in enumerate(lines2):
                if line1==line2:
                    i+=1
        per1 = i/len(lines2)
        per2 = i/len(lines1)

        dic1 = {filename:float(str(per1)[:4])}
        dic2 = {filename:float(str(per2)[:4])}
        return [dic1,dic2]


def main():
    path1 = '4_evaluation/prediction_train/'
    path2 = '4_evaluation/true_train/'
    path3 = '4_evaluation/percentage/datas_train.csv'
    with open(path3,'w',encoding='utf8',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'recall_rate','accuracy'])
        L1 = os.listdir(path1)
        L2 = os.listdir(path2)
        for i,name in enumerate(L1):
            s1 = compare(path1+name,path2+L2[i],name)

            writer.writerow([name[:-4], s1[0][name],s1[1][name]])

if __name__ == '__main__':
    main()
