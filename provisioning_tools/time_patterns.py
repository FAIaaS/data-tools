#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def minutes_patterns(mins):
    state=None
    begin=None
    highs = {}
    for i in range(60):
        if mins[i] != state:
            state = mins[i]
            if mins[i]:
                if begin == None:
                    begin = i
            else:
                begin = None 
        if mins[i]:
            if begin in highs:
                highs[begin] += 1
            else:
                highs[begin] = 1

    return highs

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: %s time_table.csv" % sys.argv[0])
        sys.exit(-1)

    errors = pd.read_csv(sys.argv[1])
    name = errors.columns[1]
    errors = errors[errors.columns[1]].values.tolist()
    patterns = minutes_patterns(errors)

    time_patterns = {name:{'start':[], 'duration':[]}}
    for tm in sorted(patterns.keys()):
        time_patterns[name]['start'].append(tm)
        time_patterns[name]['duration'].append(patterns[tm])

    print(time_patterns)
    #time_table = pd.DataFrame(time_table)
    #time_table.to_csv(sys.argv[1][:-4] + '.time_table.csv')
