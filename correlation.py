#!/usr/bin/python3

import csv
import sys
import numpy as np
from scipy.stats import pearsonr

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s csv column" % sys.argv[0])
        sys.exit(-1)

    #column1 = 1
    column1 = 3
    column2 = int(sys.argv[2])
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile)
        data1 = []
        data2 = []
        header = reader.__next__()
        name1= header[column1]
        name2= header[column2]
        for row in reader:
            #timestamp, num, delta, err
            if row[column2]:
                data1.append(float(row[column1]))
                data2.append(float(row[column2]))
            
        csvfile.close()

    corr = np.corrcoef(data1, data2)[0,1]
    pearson = pearsonr(data1, data2)

    #print("%s - %s: corr=%f pearson=%s" % (name1, name2, corr, pearson))
    print("%s - %s: pearson=%s" % (name1, name2, pearson))
    



