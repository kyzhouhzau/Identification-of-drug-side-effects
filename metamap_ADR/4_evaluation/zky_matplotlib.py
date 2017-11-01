#! usr/bin/env python3
# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
file = '4_evaluation/percentage/datas_train.csv'
data = pd.read_csv(file)
y1=data['recall_rate']
y2=data['accuracy']
x=data['name']
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
ax.bar(x,y1,color='green')
ax.bart(x,y2,color='red')
plt.ylim(0,1)
labels = ax.set_xticklabels(x,rotation=30,fontsize='5')
title = ax.set_title('Results Compare')
xlabel = ax.set_xlabel('names')
ylabel = ax.set_ylabel('percentage')
ax.legend(loc='upper right')
fig.savefig('4_evaluation/train_.png')