#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

def prepare(df, columns):
    df['Time'] = pd.to_datetime(df.Time)
    df['unavailable'] = df['Successful attempts'] < 5

    return df

def get_limits(dfi, columns):
    limits={'measurements':[
        'access_mean','access_std_deviation','access_level',
        'errors_mean','errors_std_deviation','errors_level']}
    for field in columns:
        limits[field]={}

        # service available
        a_select = dfi.loc[(dfi['unavailable'] == False)][field]
        a_mean = np.mean(a_select)
        a_std = np.std(a_select)
        a_level = a_mean + a_std

        # service unavailable
        u_select = dfi.loc[(dfi['unavailable'] == True)][field]
        u_mean = np.mean(u_select)
        u_std = np.std(u_select)
        u_level = u_mean - u_std
        limits[field] = [a_mean, a_std, a_level,
                         u_mean, u_std, u_level]
            
    return limits

def limits_cmp(dfi, limits):
    # Sucessfull accesss
    dfr = pd.DataFrame()
    dfr['Time']=dfi['Time']
    dfr['unavailable']=dfi['unavailable']

    for field in dfi.keys()[2:]:
        value = limits[limits.measurements == 'access_level'][field].values[0]
        dfr[field] = dfi[field] >= value
    
    size=len(dfr)
    for field in dfr.keys()[2:]:
        length = len(dfr[(dfr['unavailable'] != dfr[field])])
        print(f"{field}: {length} ({length/(size/100)}%)")

    # Unsucessfull access
    dfr = pd.DataFrame()
    dfr['Time']=dfi['Time']
    dfr['unavailable']=dfi['unavailable']

    for field in dfi.keys()[2:]:
        value = limits[limits.measurements == 'errors_level'][field].values[0]
        dfr[field] = dfi[field] >= value

    size=len(dfr)
    for field in dfr.keys()[2:]:
        length = len(dfr[(dfr['unavailable'] != dfr[field])])
        print(f"{field}: {length} ({length/(size/100)}%)")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: %s data.csv limits.csv columns..." % sys.argv[0])
        sys.exit(-1)

    df = pd.read_csv(sys.argv[1])
    columns = sys.argv[3:]
    dfi = prepare(df, columns)

    limits = get_limits(dfi, columns)
    if limits:
        limits = pd.DataFrame(limits)
        print(limits.columns[-1])
        limits.rename(columns={"Unnamed: 0": 'parameters'},inplace=True)
        print(limits)

        name = sys.argv[2]
        limits.to_csv(name)
        print(f"Limits saved to file {name}")

        #limits_cmp(dfi, limits)
