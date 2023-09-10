#!/usr/bin/python3

from datetime import datetime
import sys
import csv

def get_time(time):
    return time[:time.find('.')-3]

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: %s web_stat.csv eden_stat.csv result.csv" % sys.argv[0])
        sys.exit(-1)

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = {}
        reader.__next__() # header
        for row in reader:
            #timestamp, num, delta, err
            t = get_time(row[0])
            data[t] = row[1:]
            
        csvfile.close()
    
    with open(sys.argv[2], newline='') as csvfile:
        reader = csv.reader(csvfile)

        reader.__next__() # header

        #timestamp,cpu_load,app_load,tx,rx,app_tx,app_rx
        tp,cpu_load,app_load,txp,rxp,app_txp,app_rxp = reader.__next__()
        tp = datetime.fromisoformat(tp)
        for row in reader:
            dt = (datetime.fromisoformat(row[0]) - tp).seconds
            tp = datetime.fromisoformat(row[0])
            
            t = get_time(row[0])
            
            if t in data:
                tx,rx,app_tx,app_rx = row[3:]
                #print(row[3:])
                data[t].extend(row[1:3])
                #data[t].append(row[2])
                data[t].extend([(int(tx) - int(txp))/dt,
                                (int(rx) - int(rxp))/dt,
                                #(int(app_tx) - int(app_txp))/dt,
                                #(int(app_rx) - int(app_rxp))/dt,
                                (int(app_rx) - int(app_rxp))/dt,
                                (int(app_tx) - int(app_txp))/dt,
                                ])
                txp,rxp,app_txp,app_rxp = tx,rx,app_tx,app_rx
            #else:
            #    print("not in msr: " + t)

        csvfile.close()

    with open(sys.argv[3], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['Time','Successful attempts','Responce time', 'Errors',
                         'CPU Load %', 'App. CPU Load %',
                         'Tx B/s', 'Rx B/s', 'App. Tx B/s', 'App. Rx B/s'])
        for t in sorted(data.keys()):
            if len(data[t]) == 9:
                row = [t,]
                row.extend(data[t])
                writer.writerow(row)
                #print(row)
            #else:
                #print("not in eden: " + t)

        csvfile.close()
    
    #print(data)

        
