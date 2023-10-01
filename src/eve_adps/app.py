# coding: utf-8

"""Edge-data micro-service

`Flask` microservice for collecting data on exceeding the limits of measured parameters.
"""

import sys
import os
from flask import Flask
import pandas as pd

from eve_adps.time_select import time_select
from eve_adps.bandwidth import bandwidth
from eve_adps.clean import clean
from eve_adps.smooth import smooth
from eve_adps.time_table import errors_per_min

bw_columns = ['Tx B', 'Rx B', 'App. Tx B', 'App. Rx B']
#columns = ['CPU Load %','App. CPU Load %', 'Tx B', 'Rx B', 'App. Tx B', 'App. Rx B']
columns = ['CPU Load %', 'Tx B', 'Rx B']
#columns = ['App. CPU Load %', 'App. Tx B', 'App. Rx B']
# File with data collected by `adps_eden_diag` program
data_file = "~/eden_measure.csv"
limits_file = "~/eden-limits.csv"

app = Flask(__name__)

@app.route("/time_table/<time_delta>")
def time_table(time_delta):
    """Collects general data on exceeding the limits of measured parameters for a selected period of time."""
    df = pd.read_csv(data_file)
    
    df = time_select(df, 'end', time_delta)

    df = bandwidth(df, bw_columns)
    names = {}
    for column in bw_columns:
        names[column] = column + '/s'
        try:
            columns[columns.index(column)] = names[column]
        except ValueError:
            pass
    df = df.rename(columns=names)
    
    df = smooth(df, columns)
    
    limits = pd.read_csv(limits_file)
    server = os.getenv('WEB_SERVER')
    errors = errors_per_min(df, limits)
    time_table = pd.DataFrame({server: errors})
    
    csv = time_table.to_csv() #index=False)

    return csv
