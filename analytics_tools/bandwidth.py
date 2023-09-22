#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def calc_bw(df, index, column):
    '''
    Calculate bandwith
    '''
    bw = (df.iloc[index][column] - df.iloc[index-1][column]) / \
        (df.iloc[index]['Time'] - df.iloc[index-1]['Time']).seconds

    return bw

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: %s data.csv bandwidth.csv columns..." % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    df['Time'] = pd.to_datetime(df.Time)
    names = {}
    for column in sys.argv[3:]:
        bws = [0,]
        for i in range(1,len(df)):
            bws.append(calc_bw(df, i, column))
        df[column] = bws
        names[column] = column + '/s'

    df = df.rename(columns=names)
    df.to_csv(sys.argv[2])
