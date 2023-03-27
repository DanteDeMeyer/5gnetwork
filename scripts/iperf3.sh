#!/bin/bash
# Check for arguments
if [ "$#" -lt 6 ]; then
    echo "Error: Not enough arguments provided. Usage: $0 <ip addr> <duration> <UDP/TCP> <log_file> <bandwidth> <Uplink/downlink>"
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
protocol=$3
log_file=/home/dante/logs/$4
bandwidth=$5
direction=$6

# Run the iperf3 and add timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo $timestamp >> "$log_file"
iperf3 -c "$ip_addr" "$protocol" -t"$duration" -b "$direction" "$bandwitdh" | awk '{print $7,$8,$9,$10}'| head -n 14 | tail -n 10 >"$log_file"
