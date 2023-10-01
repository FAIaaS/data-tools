#!/usr/bin/env python
# coding: utf-8
"""Clear data from outliers

Removing points from the data that exceed a reasonable level.
"""
import pandas as pd

def clean(df, limits, columns):
    """Removes points greater than the average parameter level for error state plus standard deviation."""
    df = df.dropna()
    for column in columns:
        mean=limits[limits.measurements == 'errors_mean'][column].values[0]
        std=limits[limits.measurements == 'errors_std_deviation'][column].values[0]
        rm = len(df[(df[column] >= mean+std)])
        df[column] = df[(df[column] < mean+std)][column]
        size = len(df)
        print(f'Removed {rm} from {size} ({rm/(size/100)}%)')
        df = df.infer_objects(copy=False)
        df = df.interpolate()
        
    return df

def main():
    import sys
    
    if len(sys.argv) < 5:
        print("Usage: %s data.csv limits.csv result.csv columns..." % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    limits = pd.read_csv(sys.argv[2])

    df = clean(df, limits, sys.argv[4:])
    df.to_csv(sys.argv[3])

if __name__ == '__main__':
    main()
