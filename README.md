# EVE-ADPS
OpenStack EVE-OS anomaly detection and proactive provisioning system

A system designed to model the proactive provisioning of a web service hosted on Edge nodes.

On the edge nodes we run virtual machines with web servers. We then use crontab to run monitoring tools and flood generators. After collecting data, the analytical system calculates the levels of Edge device parameters (CPU load and network traffic) at which web servers become unavailable. Edge nodes then collect this data and calculate periods of time when these levels are exceeded. Such time tables are parsed by the central system and crontable entries are generated to switch the web service between edge nodes. To do this, a special tool is launched that starts the virtual machine on the activated host and stops it on the deactivated one with the corresponding change in the entry in the /etc/hosts file.

Directories:
* web-server -- a simple implementation of Shell-driven web-server.
* data -- headers of files for edge-side measurement and external access testing of web-servers.
* src -- folder with sources of Python package `eve_adps`.

## Preparation
```
pip install numpy scipy pandas flask
make
```

## Testbed confguring

Example of testebed's crontabs -- on the main system:
```
# Testing web service availability with 10 attempts per minute
* * * * *	adps_measure http://web-server1:8000 10 /home/os/web-server1.csv
* * * * *	adps_measure http://web-server2:8000 10 /home/os/web-server2.csv
# Flood generation
15,45 * * * * adps_flood http://web-server1:8000 5 # 5 min flood of web-server1 at 15 and 45 mins
0,30 * * * * adps_flood http://web-server2:8000 10 # 10 min flood of web-server2 at 0 and 40 mins
```
On Edge nodes every minute we collect statistical data for the web-server application VM (with name f8f9efe6-b015-4f87-963f-4141f4e11b65):
```
* * * * *       /home/eden/venv/bin/adps_eden_diag f8f9efe6-b015-4f87-963f-4141f4e11b65 >> ~/eden_measure.csv
```

## System Calibration

After collecting monitoring data from the central computer and edge nodes, we must analyze it. We need to do bandwidth calculation, spline smoothing, data cleaning and re-smoothing. The main result is a CSV file with the binarization limits of the measured parameters for the Edge node:
```
$ bin/analysis.sh eden1_measure.csv web-server1.csv web-server1
$ bin/analysis.sh eden2_measure.csv web-server2.csv web-server2
```
At this point we will get the files `eden1_measure.cleared.limits.csv` and `eden2_measure.cleared.limits.csv` which need to be placed on the edge node side as `eden-limits.csv` in the home directory of the user who is running the utility `eden`.

## Setup of anomaly detection and proactive provisioning

For testing purposes, we will leave only one web service availability test (note: other monitoring tasks should be disabled to avoid interference):
```
* * * * *       adps_measure http://web-server:8000 10 /home/os/web-server.csv
```

Now we need to launch the `Flask` microservice for collecting time_series data on exceeding the limits of measured parameters on the nodes:
```
$ cd ~/venv/lib/python3.10/site-packages/eve_adps
$ WEB_SERVER=web-server1 flask run --host=0.0.0.0
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.122.139:5000
Press CTRL+C to quit
```
And then configure the launch of the anomalies monitoring service on the central computer via crontab every hour:
```
0 * * * *       /usr/local/bin/anomalies_monitor.sh
```
## System operation
Anomalies monitor will attempt to find hourly patterns of high node load every hour and automagically create crontab entries to proactively switch the web service from one node to another, like this:
```
8 * * * * /usr/local/bin/switch_web-server.sh web-server1 web-server2 # autogenerated web-server switcher
14 * * * * /usr/local/bin/switch_web-server.sh web-server2 web-server1 # autogenerated web-server switcher
38 * * * * /usr/local/bin/switch_web-server.sh web-server1 web-server2 # autogenerated web-server switcher
44 * * * * /usr/local/bin/switch_web-server.sh web-server2 web-server1 # autogenerated web-server switcher
```
In the default configuration, the full cycle of setting up the crontab after changing the flood scheme is around 3 hours.
