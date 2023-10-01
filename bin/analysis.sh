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
echo bandwidth $EVE_CSV $BW_CSV \'Tx B\' \'Rx B\' \'App. Tx B\' \'App. Rx B\'
bandwidth $EVE_CSV $BW_CSV 'Tx B' 'Rx B' 'App. Tx B' 'App. Rx B'

SM_CSV=`echo $EVE_CSV | sed 's/\.csv/\.smoothed.csv/'`
echo smooth $BW_CSV $SM_CSV \'CPU Load %\' \'Tx B/s\' \'Rx B/s\' \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
smooth $BW_CSV $SM_CSV 'CPU Load %' 'Tx B/s' 'Rx B/s' 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

BWS_CSV=`basename $2`
RS_CSV=`echo $EVE_CSV $BWS_CSV | sed 's/\.csv//; s/ /./'`
echo join $SM_CSV $WS_CSV $RS_CSV
join $SM_CSV $WS_CSV $RS_CSV

LM_CSV=`echo $EVE_CSV | sed 's/\.csv/\.limits.csv/'`
echo analysis $RS_CSV $LM_CSV \'CPU Load %\' \'Tx B/s\' \'Rx B/s\' \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
analysis $RS_CSV $LM_CSV 'CPU Load %' 'Tx B/s' 'Rx B/s' 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

#echo time_patterns $SM_CSV $LM_CSV
#time_patterns $SM_CSV $LM_CSV

# Clean data
SMC_CSV=`echo $SM_CSV | sed 's/\.csv/\.cleared.csv/'`
echo clean $BW_CSV $LM_CSV $SMC_CSV \'CPU Load %\' \'Tx B/s\' \'Rx B/s\' \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
clean $BW_CSV $LM_CSV $SMC_CSV 'CPU Load %' 'Tx B/s' 'Rx B/s' 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

SMC2_CSV=`echo $SMC_CSV | sed 's/\.csv/\.smoothed.csv/'`
echo smooth $SMC_CSV $SMC2_CSV \'CPU Load %\' \'Tx B/s\' \'Rx B/s\' \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
smooth $SMC_CSV $SMC2_CSV 'CPU Load %' 'Tx B/s' 'Rx B/s' 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

RSC_CSV=`echo $RS_CSV | sed 's/\.csv/\.cleared.csv/'`
echo join $SMC2_CSV $WS_CSV $RSC_CSV
join $SMC2_CSV $WS_CSV $RSC_CSV

LMC_CSV=`echo $LM_CSV  | sed 's/\.csv/\.cleared.csv/'`
echo analysis $RSC_CSV $LMC_CSV \'CPU Load %\' \'Tx B/s\' \'Rx B/s\' \'App. CPU Load %\' \'App. Tx B/s\' \'App. Rx B/s\'
analysis $RSC_CSV $LMC_CSV 'CPU Load %' 'Tx B/s' 'Rx B/s' 'App. CPU Load %' 'App. Tx B/s' 'App. Rx B/s'

#echo time_patterns $SMC2_CSV $LMC_CSV
#time_patterns $SMC2_CSV $LMC_CSV

TT_CSV="$DOC_DIR/$SRV.time_table.csv"
echo time_table $SMC2_CSV $LMC_CSV $SRV $TT_CSV
time_table $SMC2_CSV $LMC_CSV $SRV $TT_CSV

