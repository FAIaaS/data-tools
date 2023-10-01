#!/usr/bin/env python
# coding: utf-8
"""Select data from a CSV file for a selected time period"""

from datetime import datetime
import pandas as pd

def time_select(df, begin, end):
    """Select data from DataFrame for a selected time period.
    Timestamps can be exact or relative:
    * begin = ['begin'|'now'|'end']
    * end = for ex. -1h or +3h
    """
    df['Time'] = pd.to_datetime(df.Time)
    df = df.sort_values(by='Time')
    
    if begin[0] == 'b': # begin
        begin = df.iloc[0]['Time']
    elif begin[0] == 'n': # now
        begin = datetime.now()
    elif begin[0] == 'e': # end
        begin = df.iloc[len(df) -1]['Time']
    else:
        begin = datetime.fromisoformat(sys.argv[3])

    if end:
        try:
            end = datetime.fromisoformat(end)
        except ValueError:
            end = begin + pd.Timedelta(end).to_pytimedelta()
        if end < begin:
            tmp = end
            end = begin
            begin = tmp
        dfs = df.loc[(df['Time'] >= begin) & (df['Time'] <= end)]
    elif begin:
        dfs = df.loc[(df['Time'] >= begin)]
    else:
        dfs = df

    print(f'{begin} {end}')
    return dfs

def main():
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: %s input.csv output.csv begin_time|begin|now|end [end_time|+time|-time]" % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    begin = end = None

    if len(sys.argv) > 3:
        begin = sys.argv[3]
    if len(sys.argv) > 4:
        end = sys.argv[4]

    dfs = time_select(df, begin, end)
    dfs.to_csv(sys.argv[2])
                    
if __name__ == '__main__':
    main()
