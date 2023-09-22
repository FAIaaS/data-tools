#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def clean(df, limits, columns):
    dfc = df
    for column in columns:
        mean=limits[limits.measurements == 'errors_mean'][column].values[0]
        std=limits[limits.measurements == 'errors_std_deviation'][column].values[0]
        rm = len(dfc[(dfc[column] >= mean+std)])
        dfc[column] = dfc[(dfc[column] < mean+std)][column]
        size = len(dfc)
        print(f'Removed {rm} from {size} ({rm/(size/100)}%)')
        dfc = dfc.interpolate()
        
    return dfc

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 5:
        print("Usage: %s data.csv limits.csv result.csv columns..." % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    limits = pd.read_csv(sys.argv[2])

    dfc = clean(df, limits, sys.argv[4:])
    dfc.to_csv(sys.argv[3])
