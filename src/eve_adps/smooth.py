#!/usr/bin/env python
# coding: utf-8
"""Smooth data in selected columns using a cubic spline"""

import pandas as pd
from scipy.interpolate import CubicSpline

def smooth(df, columns):
    """Filling non-existent points and smoothing all data with a cubic spline""" 
    df = df.dropna()
    for field in columns:
        i = CubicSpline(df.index, df[field])
        df.loc[:, [field]] = i(df.index)

    return df

def main():
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: %s data.csv smoothed.csv columns..." % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    dfi = smooth(df, sys.argv[3:])
    dfi.to_csv(sys.argv[2])

if __name__ == '__main__':
    main()
