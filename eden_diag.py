#!/usr/bin/python3

import subprocess
import json
import collections
import datetime
import sys

eden = '/home/eden/eden/eden'

def eden_dinfo():
    info = {}
    result = subprocess.run(
        [eden, 'info', '--format', 'json'],
        stdout=subprocess.PIPE)
    if result.stdout:
        out = result.stdout.decode("utf-8")
        #LOG.debug('EDEN stdout: ' + out)
        out = out.split('\n')
        infos = len(out)
        for i in range(0, infos):
            try:
                info = json.loads(out[infos - 1 - i])
                if 'dinfo' in info:
                    info = info["dinfo"]
                    break
            except json.decoder.JSONDecodeError:
                continue

    return info

def eden_metric():
    metric = {}
    result = subprocess.run(
        [eden, 'metric', '--format=json', '--tail', '1'],
        stdout=subprocess.PIPE)
    if result.stdout:
        out = result.stdout.decode("utf-8")
        #LOG.debug('EDEN stdout: ' + out)
        metric = json.loads(out)

    return metric

def eden_pod_ps():
    apps = []
    result = subprocess.run(
        [eden, 'pod', 'ps', '--format=json'],
        stdout=subprocess.PIPE)
    if result.stdout:
        out = result.stdout.decode("utf-8")
        #LOG.debug('EDEN stdout: ' + out)
        apps = json.loads(out)

    return apps

def eden_measure(name):
    timestamp = datetime.datetime.now().isoformat()

    # CPU Load
    result = subprocess.run(
        [eden, 'metric', '--format=json', '--tail', '2',
         '--out', 'dm.cpuMetric.totalNs'],
        stdout=subprocess.PIPE)
    ns = result.stdout.decode('utf-8').split('\n')
    result = subprocess.run(
        [eden, 'metric', '--format=json', '--tail', '2',
         '--out', 'dm.cpuMetric.upTime.seconds'],
        stdout=subprocess.PIPE)
    s = result.stdout.decode('utf-8').split('\n')
    cpu_load = ((int(ns[1]) - int(ns[0]))/(int(s[1]) - int(s[0])))/1000000000
    
    info = eden_dinfo()
   
    nw = eden_metric()['dm']["network"][2]
    rx = nw["rxBytes"]
    tx = nw["txBytes"]
    
    apps = eden_pod_ps()
    for app in apps:
        if app['Name'] == name:
            app_load = app['CPUUsage']
            
    metric = eden_metric()
    if 'am' in metric:
        apps = metric['am']

        for app in apps:
            if app['AppName'] == name:
                nw = app['network'][0]
                app_tx = nw['txBytes']
                app_rx = nw['rxBytes']

    return(timestamp,cpu_load,app_load,tx,rx,app_tx,app_rx)

if __name__ == '__main__':
    timestamp,cpu_load,app_load,tx,rx,app_tx,app_rx = eden_measure(sys.argv[1])
    print("%s,%s,%s,%s,%s,%s,%s" % (timestamp,cpu_load,app_load,tx,rx,app_tx,app_rx))
