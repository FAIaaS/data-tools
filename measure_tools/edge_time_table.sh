#!/bin/bash

if [ $# -lt 2 ]
then
	echo "Usage: $0 eve_diag.csv limits.csv server_name"
	exit -1
fi

EVE_CSV=$1
LMC_CSV=$2
SRV=$3
DOC_DIR=`dirname $EVE_CSV`

BW_CSV=`echo $EVE_CSV | sed 's/\.csv/\.bw.csv/'`
echo python bin/bandwidth.py $EVE_CSV $BW_CSV \'App. Tx B\' \'App. Rx B\'
python bin/bandwidth.py $EVE_CSV $BW_CSV 'App. Tx B' 'App. Rx B'

# Clean data
SMC_CSV=`echo $SM_CSV | sed 's/\.csv/\.cleared.csv/'`
echo python bin/clean.py $BW_CSV $LM_CSV $SMC_CSV \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
python bin/clean.py $BW_CSV $LM_CSV $SMC_CSV 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

SMS_CSV=`echo $SMC_CSV | sed 's/\.csv/\.smoothed.csv/'`
echo python bin/smooth.py $SMC_CSV $SMS_CSV \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
python bin/smooth.py $SMC_CSV $SMS_CSV 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

#echo python bin/time_patterns.py $SMC2_CSV $LMC_CSV
#python bin/time_patterns.py $SMC2_CSV $LMC_CSV

TT_CSV="$DOC_DIR/$SRV.time_table.csv"
echo python bin/time_table.py $SMC_CSV $LMC_CSV $SRV $TT_CSV
python bin/time_table.py $SMC_CSV $LMC_CSV $SRV $TT_CSV

