#!/usr/bin/env python
# coding: utf-8

import pandas as pd

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: %s web-server.csv eden.csv result.csv" % sys.argv[0])
        sys.exit(-1)

    srv = pd.read_csv(sys.argv[1])
    srv['Time'] = pd.to_datetime(srv.Time)
    eden = pd.read_csv(sys.argv[2])
    eden['Time'] = pd.to_datetime(eden.Time)
    result = pd.merge_asof(srv, eden, on='Time')
    result.to_csv(sys.argv[3])
