#!/usr/bin/python3

import csv
import sys
import math
import numpy

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s csv column" % sys.argv[0])
        sys.exit(-1)

    column = int(sys.argv[2])
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        name = reader.__next__()[column] # header
        for row in reader:
            #timestamp, num, delta, err
            if row[2]:
                data.append(float(row[column]))
            
        csvfile.close()

    print("%s: %6f ± %f" % (name,numpy.mean(data),numpy.std(data)))
