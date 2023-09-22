#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from scipy.interpolate import CubicSpline

def smooth(df, columns):
    dfi = df

    for field in columns:
        i = CubicSpline(dfi.index, dfi[field])
        dfi[field] = i(dfi.index)

    return dfi

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: %s data.csv smoothed.csv columns..." % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    dfi = smooth(df, sys.argv[3:])
    dfi.to_csv(sys.argv[2])
