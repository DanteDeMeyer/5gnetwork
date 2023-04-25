#!/bin/bash
set -e
# Check if enough arguments were provided
if [ "$#" -lt 3 ]; then
    echo "Error: Not enough arguments provided. Usage: $0 <ip addr> <duration> <log_file>"
    exit 1
fi

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
log_file=/home/dante/logs/$3
measurement=$4
#run ping command and log results
for (( i=1; i<=$duration; i++ ))
do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    latency=$(ping -c 1 "$ip_addr" | awk -F'=' '/time/ {print $4}' | sed 's/ms//')
    echo "$measurement,\"$timestamp\",$latency"
    echo "measurement,\"$timestamp\",$latency" >> "$log_file"
    sleep 1
done
