#!/bin/bash

# Define variables
log_file_name=$(echo "$1" | sed 's/\.[^.]*$//')
log_file=/home/dante/logs/$log_file_name.csv

# Run iperf3 and extract jitter using jq, then append to log file
jitter=$(iperf3 -s -J | jq -r '.intervals[] | [.streams[0].jitter_ms] | @csv')
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "$timestamp,$jitter" >> "$log_file"

# Print completion message
echo "iperf3 server successfully done and jitter saved in $log_file"
