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

# Run the iperf3 command for the specified duration, with a sleep of 1 second between each iteration
for (( i=1; i<=$duration; i++ ))
do
    # Run iperf3 and extract timestamp and bitrate using jq, then append to log file
    iperf3 -c "$ip_addr" "$protocol" -b  "$direction" "$bandwitdh" -t 1 -J | jq -r '.start.timestamp as $start | .intervals[] | [($start.timesecs | strftime("%Y-%m-%d %H:%M:%S")), (.streams[0].bits_per_second/1000000)] | @csv' >> "$log_file"
    sleep 1
done

# Print completion message
echo iperf3 successfully done for $2 seconds to $1 saved in "$log_file"
