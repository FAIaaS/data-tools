#!/usr/bin/python3

import csv
import sys
import numpy
from scipy.stats import pearsonr

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s csv erros.csv" % sys.argv[0])
        sys.exit(-1)

    #column1 = 1
    err_column = 3
    with open(sys.argv[2], newline='') as csvfile:
        reader = csv.reader(csvfile)
        table = {}
        for row in reader:
            table[int(row[0])] = {'mean': float(row[1]),
                                  'dev': float(row[2])}

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile)
        columns = max(table.keys()) + 1
        ok = [0 for i in range(columns)]
        no = [0 for i in range(columns)]
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
                    if int(row[err_column]) < 5 and val < threshold or \
                       int(row[err_column]) >= 5 and val > threshold:
                        vote += 1
                        ok[i] += 1
                        print("OK -- %s, %s, %f, %f" %
                              (time, row[err_column], val, threshold))
                    else:
                        no[i] += 1
                        print("NO -- %s, %s, %f, %f" %
                              (time, row[err_column], val, threshold))
            if vote >= len(table.keys())/2:
                votes += 1
            
        csvfile.close()

        for i in table.keys():
            print("%s = %f%%" % (header[i], no[i]/(ok[i]/100)))

        print("votes: %f" % ((num-votes)/(num/100)))

