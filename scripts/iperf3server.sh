#!/bin/bash

# Define variables
log_file_name=$(echo "$1" | sed 's/\.[^.]*$//')
log_file=/home/dante/logs/$log_file_name.csv

# Run the iperf3 and add timestamp
if [iperf -s == "Server listening on 5201"]; then
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo $timestamp >> "$log_file"
iperf3 -s | awk '{print $7,$8,$9,$10}'| head -n 14 | tail -n 10

