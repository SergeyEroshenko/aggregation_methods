#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import pandas as pd
import numpy as np

def dtypes_corr(df):
    
    """Convert RAW data to Pandas dtypes"""
    
    df = df.astype({
        'timestamp':'datetime64[ns]',
        'id': 'int64',
        'price': 'float64',
        'quantity': 'float64'
    })
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    df['amount'] = 1
    df['side'] = df['side'].map({'buy':1, 'sell':-1})*df['quantity']
    df = df.drop(df.columns[0], axis=1)
    
    return df


def fill_empty(df):
    
    df = df.copy()
    ret = []
    last_index = 0
    cols = df.shape[1]
    col_names = df.columns
    
    indexes = np.where(np.diff(df.index.values)>1)[0]+1
    nums = np.diff(df.index.values)-1
    nums = nums[nums!=0]
    values = df.iloc[np.where(np.diff(df.index.values)>1)[0]+1]['open']
    
    for idx, (index, num, value) in enumerate(zip(indexes, nums, values)):
        add = pd.DataFrame(np.zeros((num, cols)), columns=col_names)
        add.iloc[:,:4]=value
        add = pd.concat([df[last_index:index], add], ignore_index=True)
        ret.append(add)
        last_index=index
    
    if len(ret)==0:
        return df
    
    return pd.concat(ret).reset_index(drop=True)


def time_repr(df, frame):
    
    """Time bars"""
    df = df.copy()
    df = df.set_index('timestamp')

    df = pd.concat([
        df.resample(frame)['price'].ohlc(),
        df.resample(frame)['quantity'].sum(),
        df.resample(frame)['side'].sum(),
        df.resample(frame)['amount'].sum()
    ], axis=1)
    
    return df


def quant_repr(df, frame):
    
    """Volume bars"""
    df = df.copy()    
    df.index = (df['quantity'].cumsum()/frame).astype('int64')

    df = pd.concat([
        df.groupby(df.index)['price'].ohlc(),
        df.groupby(df.index)['side'].sum(),
        df.groupby(df.index)['amount'].sum()
    ], axis=1)

    return df


def tick_repr(df, frame):
    
    """Tick bars"""
    
    df = df.reset_index()
    df.index = (df.index.values/frame).astype('int64')

    df = pd.concat([
        df.groupby(df.index)['price'].ohlc(),
        df.groupby(df.index)['side'].sum(),
        df.groupby(df.index)['quantity'].sum()
    ], axis=1)

    return df


def money_repr(df, frame):
    
    """Money bars"""
    df = df.copy()    
    df.index = (
        (df['quantity']*df['price']).cumsum()/frame
    ).astype('int64')

    df = pd.concat([
        df.groupby(df.index)['price'].ohlc(),
        df.groupby(df.index)['side'].sum(),
        df.groupby(df.index)['amount'].sum()
    ], axis=1)

    return df
