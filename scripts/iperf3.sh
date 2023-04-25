#!/bin/bash

# Validate input
if ! ping -t1 -c 1 "$1" > /dev/null 2>&1; then
    echo "Error: Invalid IP address provided."
    exit 1
fi

# Define variables
ip_addr=$1
log_file_name=$(echo "$2" | sed 's/\.[^.]*$//')
log_file=/home/dante/logs/$log_file_name.csv

# Get current date and time
datetime=$(date +"%Y-%m-%d %H:%M:%S")

# Run iperf3 and extract bitrate and jitter using awk
iperf_output=$(iperf3 -c "$ip_addr" -u -b 100M -R)
bitrate=$(echo "$iperf_output" | grep receiver | awk '{print $7}')
jitter=$(echo "$iperf_output" | grep receiver | awk '{print $9}')

# Print results to console
echo "$datetime,$bitrate,$jitter"

# Append results to CSV log file
echo "$datetime,$bitrate,$jitter" >> "$log_file"
