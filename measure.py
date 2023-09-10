#!/usr/bin/python3

import requests
import datetime
import sys
import urllib3
import time
import csv
from filelock import FileLock

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s url num_of_queries" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    limit = sys.argv[2]
    #file = "/data/work/sadov/LastCloud.AI/kolla-ansible/measurements.csv"
    file = sys.argv[3]
    
    num = 0
    err = 0
    delta=datetime.timedelta()

    timestamp = datetime.datetime.now().isoformat()
    print("time: " + timestamp)
    for i in range(0,int(limit)):
        try:
            t1=datetime.datetime.now()
            #requests.get('http://172.16.0.79:8000/')
            requests.get(url)
            t2=datetime.datetime.now()
            num += 1
            #print("delta=%s\n" % (t2-t1))
            delta += t2-t1
            time.sleep(0.2)
        except urllib3.exceptions.MaxRetryError:
            err += 1
        except requests.exceptions.ConnectionError:
            err += 1
        except  Exception as error:
            # handle the exception
            print("An exception occurred:", type(error).__name__, "–", error)

    if num:
        delta = delta/num
    else:
        delta = ''

    print("passed=%d (%s) " % (num, delta))
    print("errors=%d\n" % err)

    lock = FileLock(file + ".lock")
    with lock:
        with open(file, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, num, delta, err])
            csvfile.close()
