# data-tools
Proactive provisioning system

A system designed to model the proactive provisioning of a web service hosted on Edge nodes.

On the edge nodes we run virtual machines with web servers. We then use crontab to run monitoring tools and flood generators. After collecting data, the analytical system calculates the levels of Edge device parameters (CPU load and network traffic) at which web servers become unavailable. Edge nodes then collect this data and calculate periods of time when these levels are exceeded. Such time tables are parsed by the central system and crontable entries are generated to switch the web service between edge nodes. To do this, a special tool is launched that starts the virtual machine on the activated host and stops it on the deactivated one with the corresponding change in the entry in the /etc/hosts file.

Directories:
* web-server -- a simple implementation of Shell-driven web-server.
* data -- headers of files for edge-side measurement and external access testing of web-servers.
* measure_tools -- tools for edge-side measurement and external access testing of web servers.
* analytics_tools -- tools for data preparation and analysis.
* provisioning_tools -- tools for generation of crontab records.

## Example of testebed's crontabs

On the main system:
```
# Testing web service availability with 10 attempts per minute
* * * * *	/usr/local/bin/measure.py http://web-server1:8000 10 /home/os/web-server1.csv
* * * * *	/usr/local/bin/measure.py http://web-server2:8000 10 /home/os/web-server2.csv
# Flood generation
15,45 * * * * /usr/local/bin/flood.py http://web-server1:8000 5 # 5 min flood at 15 and 45 mins
0,30 * * * * /usr/local/bin/flood.py http://web-server2:8000 10 # 10 min flood at 0 and 40 mins
```
On Edge nodes every minute we collect statistical data for the web-server application VM with id 287dff0a-2996-4c2d-8f42-288ac315f4c1:
```
* * * * *       /usr/local/bin/eden_diag.py 287dff0a-2996-4c2d-8f42-288ac315f4c1 >> ~/eden1_measure.csv
```

## Possible scenario

Bandwidth calculation, spline smoothing, data cleaning and re-smoothing. The main result is a CSV file with the binarization limits of the measured parameters for the Edge node:
```
$ bin/analysis.sh eden1_measure.csv web-server1.csv web-server1
$ bin/analysis.sh eden2_measure.csv web-server2.csv web-server2
```
At this point we will get the `eden1_measure.cleared.limits.csv` and `eden2_measure.cleared.limits.csv` files, which can be used on the edge node side to create time-tables:
```
$ bin/edge_time_table.sh eden1_measure.csv eden1_measure.limits.cleared.csv web-server1
$ bin/edge_time_table.sh eden2_measure.csv eden2_measure.limits.cleared.csv web-server2

```
We now have binarized time-tables from edge nodes that reflect the availability of web services: `web-server1.time_table.csv` and `web-server2.time_table.csv`. And finally, let's create crontab entries from edge-node time-tables:
```
$ python bin/switcher.py /usr/local/bin/switch_web-server.sh web-server1.time_table.csv web-server2.time_table.csv

```

## Generated crontab web-service switching tasks

As we can see, our web-service must be switched proactively, in accordance with the found time-series patterns and taking into account the service switching delay at the edge-nodes:
```
8 * * * * /usr/local/bin/switch_web-server.sh web-server1 web-server2 # autogenerated web-server switcher
13 * * * * /usr/local/bin/switch_web-server.sh web-server2 web-server1 # autogenerated web-server switcher
38 * * * * /usr/local/bin/switch_web-server.sh web-server1 web-server2 # autogenerated web-server switcher
43 * * * * /usr/local/bin/switch_web-server.sh web-server2 web-server1 # autogenerated web-server switcher
```
