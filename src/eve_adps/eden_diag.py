#!/usr/bin/python3
"""Collection of EDEN diagnostics

Getting total EVE CPU load, application CPU load, network traffic from EVE network interface and application network interface.
"""
import subprocess
import json
import collections
import datetime
import sys

eden = '/home/eden/eden/eden'

def eden_dinfo():
    """Get `eden info`"""
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
    """Get `eden metric`"""
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
    """Get `eden metricpod ps`"""
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
    """Get EVE CPU load, application CPU load, network traffic from EVE network interface and application network interface"""
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
    
    #info = eden_dinfo()
   
    metric = eden_metric()
    nw = metric['dm']["network"][2]
    rx = nw["rxBytes"]
    tx = nw["txBytes"]
    
    apps = eden_pod_ps()
    for app in apps:
        if app['Name'] == name:
            app_load = app['CPUUsage']
            
    if 'am' in metric:
        apps = metric['am']

        for app in apps:
            if app['AppName'] == name:
                if 'network' in app:
                    nw = app['network'][0]
                    if 'txBytes' in nw:
                        app_tx = nw['txBytes']
                    else:
                        app_tx = 0
                    if 'rxBytes' in nw:
                        app_rx = nw['rxBytes']
                    else:
                        app_rx = 0
                else:
                    app_tx = 0
                    app_rx = 0

    return(timestamp,cpu_load,app_load,tx,rx,app_tx,app_rx)

def main():
    timestamp,cpu_load,app_load,tx,rx,app_tx,app_rx = eden_measure(sys.argv[1])
    print("%s,%s,%s,%s,%s,%s,%s" % (timestamp,cpu_load,app_load,tx,rx,app_tx,app_rx))
    
if __name__ == '__main__':
    main()
