#!/usr/bin/python3

import csv
import sys
import numpy
from scipy.stats import pearsonr

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s csv column" % sys.argv[0])
        sys.exit(-1)

    column1 = 3
    column2 = int(sys.argv[2])
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile)
        err = []
        header = reader.__next__()
        name= header[column2]
        for row in reader:
            #timestamp, num, delta, err
            if row[column2]:
                if int(row[column1]) >= 5:
                    err.append(float(row[column2]))
            
        csvfile.close()

    print("%d,%f,%f" % (column2,numpy.mean(err),numpy.std(err)))
    



