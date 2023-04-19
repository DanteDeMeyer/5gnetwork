#!/bin/bash

# Validate input
if ! ping -t1 -c 1 "$1" > /dev/null 2>&1; then
    echo "Error: Invalid IP address provided."
    exit 1
fi

if ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Error: Duration must be a positive integer."
    exit 1
fi

# Define variables
ip_addr=$1
duration=$2
protocol=$6
log_file_name=$(echo "$3" | sed 's/\.[^.]*$//')
log_file=/home/dante/logs/$log_file_name.csv
bandwidth=$4
direction=$5

# Run the iperf3 and add timestamp
for (( i=1; i<=$duration; i++ ))
do
    iperf3 -c "$ip_addr" "$protocol" -b  "$direction" "$bandwitdh" -t 1 -J | jq -r '.start.timestamp.timesecs as $start | .intervals[] | [(($start | tonumber), (.streams[0].bits_per_second/1000000), (.streams[0].jitter_ms))] | @csv'| awk -F, '{print strftime("%Y-%m-%d %H:%M:%S", $1), $2, $3}' >> "$log_file"
done
echo iperf3 successfully done for $2 seconds to $1
