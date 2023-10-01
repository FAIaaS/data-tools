#!/usr/bin/env python
# coding: utf-8
"""Anomaly detector

Detects anomalies by counting errors during attempts to access a monitored service.
"""

import pandas as pd

def detect_anomaly(df, column, limit):
    """Detects anomalies by counting values that exceed a `limit` in a `column`."""
    df['Time'] = pd.to_datetime(df.Time)
        
    df[column] = df[column] >= limit
    errs = df[column].sum()
    size = len(df[column])
    prct = errs/(size/100)

    return errs, size, prct

def main():
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: %s data.csv column limit" % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    column = sys.argv[2]
    limit = float(sys.argv[3])

    errs, size, prct = detect_anomaly(df, column, limit)
    #print(f'In "{column}" {errs} errors in {size} measurements ({prct}%)')
    print(round(prct))

if __name__ == '__main__':
    main()
