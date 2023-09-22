#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def errors_per_min(dfi, limits):
    dfr = pd.DataFrame()
    dfr['Time'] = pd.to_datetime(dfi.Time)
    columns = limits.keys()[2:]

    for field in columns:
        value = limits[limits.measurements == 'errors_level'][field].values[0]
        dfr[field] = dfi[field] >= value
 
              
    for field in columns:
        dfr[field] = dfr[field].astype(int)
        
    dfr['higher'] = dfr.loc[:, columns].sum(axis=1) > 1

    dfr['minute']=dfr['Time'].dt.minute

    mins = [dfr.loc[dfr['minute'] == minute, 'higher'].sum() for \
            minute in range(60)]

    mmid=(max(mins)-min(mins))/2

    for i in range(60):
        mins[i] = 1 if mins[i] >= mmid else 0

    return mins

if __name__ == '__main__':
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
