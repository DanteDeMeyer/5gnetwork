#!/bin/bash

# Validate input
if ! ping -t1 -c 1 "$1" > /dev/null 2>&1; then
    echo "Error: Invalid IP address provided."
    exit 1
fi

# Define variables
ip_addr=$1
log_file_name=$(echo "$3" | sed 's/\.[^.]*$//')
log_file=/home/dante/logs/$log_file_name.csv

# Run the iperf3 command for the specified duration, with a sleep of 1 second between each iteration
    # Run iperf3 and extract timestamp and bitrate using jq, then append to log file
    iperf3 -c "$ip_addr" -u -b  100m -R -J | jq -r '.start.timestamp as $start | .end | [($start.timesecs | strftime("%Y-%m-%d %H:%M:%S")), (.streams[0].bits_per_second/1000000), (.streams[0].jitter_ms)] | @csv' >> "$log_file"

# Print completion message
echo iperf3 successfully to $1 saved in "$log_file"
