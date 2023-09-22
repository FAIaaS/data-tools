#!/bin/bash

if [ $# -lt 2 ]
then
	echo "Usage: $0 eve_diag.csv ws_diag.csv server_name"
	exit -1
fi

EVE_CSV=$1
WS_CSV=$2
SRV=$3
DOC_DIR=`dirname $EVE_CSV`

BW_CSV=`echo $EVE_CSV | sed 's/\.csv/\.bw.csv/'`
echo python bin/bandwidth.py $EVE_CSV $BW_CSV \'App. Tx B\' \'App. Rx B\'
python bin/bandwidth.py $EVE_CSV $BW_CSV 'App. Tx B' 'App. Rx B'

SM_CSV=`echo $EVE_CSV | sed 's/\.csv/\.smoothed.csv/'`
echo python bin/smooth.py $BW_CSV $SM_CSV \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
python bin/smooth.py $BW_CSV $SM_CSV 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

BWS_CSV=`basename $2`
RS_CSV=`echo $EVE_CSV $BWS_CSV | sed 's/\.csv//; s/ /./'`
echo python bin/join.py $SM_CSV $WS_CSV $RS_CSV
python bin/join.py $SM_CSV $WS_CSV $RS_CSV

LM_CSV=`echo $EVE_CSV | sed 's/\.csv/\.limits.csv/'`
echo python bin/analysis.py $RS_CSV $LM_CSV \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
python bin/analysis.py $RS_CSV $LM_CSV 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

#echo python bin/time_patterns.py $SM_CSV $LM_CSV
#python bin/time_patterns.py $SM_CSV $LM_CSV

# Clean data
SMC_CSV=`echo $SM_CSV | sed 's/\.csv/\.cleared.csv/'`
echo python bin/clean.py $BW_CSV $LM_CSV $SMC_CSV \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
python bin/clean.py $BW_CSV $LM_CSV $SMC_CSV 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

SMC2_CSV=`echo $SMC_CSV | sed 's/\.csv/\.smoothed.csv/'`
echo python bin/smooth.py $SMC_CSV $SMC2_CSV \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
python bin/smooth.py $SMC_CSV $SMC2_CSV 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

RSC_CSV=`echo $RS_CSV | sed 's/\.csv/\.cleared.csv/'`
echo python bin/join.py $SMC2_CSV $WS_CSV $RSC_CSV
python bin/join.py $SMC2_CSV $WS_CSV $RSC_CSV

LMC_CSV=`echo $LM_CSV  | sed 's/\.csv/\.cleared.csv/'`
echo python bin/analysis.py $RSC_CSV $LMC_CSV \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
python bin/analysis.py $RSC_CSV $LMC_CSV 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

#echo python bin/time_patterns.py $SMC2_CSV $LMC_CSV
#python bin/time_patterns.py $SMC2_CSV $LMC_CSV

TT_CSV="$DOC_DIR/$SRV.time_table.csv"
echo python bin/time_table.py $SMC2_CSV $LMC_CSV $SRV $TT_CSV
python bin/time_table.py $SMC2_CSV $LMC_CSV $SRV $TT_CSV

