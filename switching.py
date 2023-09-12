#!/usr/bin/python3

import csv
import sys
import numpy
from scipy.stats import pearsonr

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s csv erros.csv" % sys.argv[0])
        sys.exit(-1)

    err_column = 3
    with open(sys.argv[2], newline='') as csvfile:
        reader = csv.reader(csvfile)
        table = {}
        for row in reader:
            table[int(row[0])] = {'mean': float(row[1]),
                                  'dev': float(row[2])}

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile)
        state = 1
        votes = 0
        num = 0
        header = reader.__next__()
        for row in reader:
            time = row[0].split('T')[-1]
            num += 1
            vote = 0
            for i in table.keys():
                if row[i]:
                    val = float(row[i])
                    threshold = table[i]['mean'] - table[i]['dev']
                    if val > threshold:
                        vote += 1
            if vote >= len(table.keys())/2:
                if state:
                    print("%s -- OFF" % time)
                    state = 0
            else:
                if state == 0:
                    print("%s -- ON" % time)
                    state = 1
                    
        csvfile.close()

