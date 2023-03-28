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

#run ping command and log results
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo $timestamp >> "$log_file"
ping -c "$duration" "$ip_addr" | awk -F'=' '/time/ {print $4}' | sed 's/ms//' >> "$log_file"