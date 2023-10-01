#!/usr/bin/env python
# coding: utf-8
"""Finding data values measured on nodes that exceed the error level from the limits file
"""

import pandas as pd

def errors_per_min(df, limits):
    """Combining measured data from a DataFrame to estimate the exceedance of an error level from a limits file"""
    df['Time'] = pd.to_datetime(df.Time)
    columns = limits.keys()[2:]

    for field in columns:
        value = limits[limits.measurements == 'errors_level'][field].values[0]
        df[field] = df[field] >= value
 
              
    for field in columns:
        df[field] = df[field].astype(int)
        
    df['higher'] = df.loc[:, columns].sum(axis=1) > 1

    df['minute']=df['Time'].dt.minute

    mins = [df.loc[df['minute'] == minute, 'higher'].sum() for \
            minute in range(60)]

    mmid=(max(mins)-min(mins))/2

    for i in range(60):
        mins[i] = 1 if mins[i] >= mmid else 0

    return mins

def main():
    import sys
    
    if len(sys.argv) < 5:
        print("Usage: %s data.csv limits.csv server_name time_table.csv" % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])

    limits = pd.read_csv(sys.argv[2])
    server = sys.argv[3]
    
    errors = errors_per_min(df, limits)

    time_table = pd.DataFrame({server: errors})

    time_table.to_csv(sys.argv[4])

if __name__ == '__main__':
    main()
