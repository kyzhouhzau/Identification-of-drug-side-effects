#! usr/bin/env python3
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
file = 'datas_train.csv'
data = pd.read_csv(file)
data.head()
t=np.arange(10)
y1=data['recall_rate']
y2=data['precision']
x=data['name']
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
ax.bar(t,y1,color='green',width=0.25)
ax.bar(t+0.25,y2,color='red',width=0.25)
plt.ylim(0,1)
labels = ax.set_xticklabels(x,rotation=30,fontsize='5')
title = ax.set_title('Results Compare')
xlabel = ax.set_xlabel('names')
ylabel = ax.set_ylabel('percentage')
recall_rate_=sum(y1)/len(y1)
precision_=sum(y2)/len(y2)
ax.add_line(Line2D(t, [recall_rate_]*len(y1), linewidth=2, color='green'))
ax.add_line(Line2D(t, [precision_]*len(y2), linewidth=2, color='red'))
fig.show()
fig.savefig('train_.png')
