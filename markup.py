#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import numpy as np

def PL_detect(slide, TP, SL):
    
    slide -= slide[0,0]
    
    a = np.where(slide[:,1]>=TP)[0]
    b = np.where(slide[:,2]<=-SL)[0]
        
    if (len(a)==0) & (len(b)==0):
        return 0

    if len(a)==0:
        a=np.array([slide.shape[0]])
    if len(b)==0:
        b=np.array([slide.shape[0]])

    if a[0] < b[0]:
        return 1
    elif a[0] > b[0]:
        return 2
    else:
        return 3
    

def window_cutter(df, TP, SL, size_0, size_1, point):

    df = df.dropna()
    df.iloc[:,0:4] = df.iloc[:,0:4]*point
    df = df.to_numpy()    
    
    dataset = []
    for i in range(size_0, df.shape[0]-size_1):
        slide = df[i:i+size_1].copy()
        label = np.array([[PL_detect(slide, TP, SL)]])
        subset = df[i-size_0:i]
        subset = subset.reshape(1, subset.size)
        subset = np.append(subset, label, axis=1)
        dataset.append(subset)

    return np.concatenate(dataset)


def select(df, data, size_0):
    
    bars = np.where(np.diff(data[:,-1])!=0)[0]+1
    stop_bar = bars[-2]

    for i in range(bars.shape[0]-1):

        d = df.loc[bars[i]+size_0:bars[i+1]+size_0-1]\
        .reset_index(drop=True)

        try:
            a = d[d['high']!=d['low']].index[0]
            bars[i] += a
        except:
            pass

    return bars

