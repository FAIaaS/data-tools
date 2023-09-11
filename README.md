# data-tools
Tools for measurement and analysis.

./data_preprocess.py measurements.csv eden_measure.csv web-server.csv
for i in 2 4 5 6 7 8 9; do ./correlation.py web-server.csv $i; done
for i in 2 4 5 6 7 8 9; do ./mean+std.py web-server.csv $i; done
for i in 2 4 5 6 7 8 9; do ./errors.py web-server.csv $i; done
for i in 2 4 5 6 7 8 9; do ./get_errors.py web-server.csv $i; done > errors.txt
for i in 5 8 9; do ./get_errors.py web-server.csv $i; done > errors-5,8,9.txt
./check.py web-server.csv errors-5,8,9.csv
./switching.py web-server.csv errors.csv > switching.txt
