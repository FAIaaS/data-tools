#!/usr/bin/python3

import requests
import urllib3
import sys
import datetime

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s url time" % sys.argv[0])
        sys.exit(-1)

wait = datetime.timedelta(minutes=float(sys.argv[2]))
t1 = datetime.datetime.now()
while 1:
    try:
        t2 = datetime.datetime.now()
        if wait < (t2-t1):
            sys.exit()
        #requests.get('http://172.16.0.79:8000/')
        requests.get(sys.argv[1])
    except urllib3.exceptions.MaxRetryError:
        pass
    except requests.exceptions.ConnectionError:
        pass

