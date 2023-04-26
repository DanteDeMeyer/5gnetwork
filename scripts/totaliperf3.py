import subprocess
import json
import csv
from datetime import datetime

# Run the iperf3 command and store the JSON data in a variable
result = subprocess.run(['iperf3', '-c', '10.45.0.1', '-u', '-b', '100M', '-R', '-J'], stdout=subprocess.PIPE)
data = json.loads(result.stdout)

# Extract the relevant data from the JSON and organize it in a dictionary
data_dict = {}
for interval in data['intervals']:
    date_time = data['start']['timestamp']['time']
    for stream in interval['streams']:
        start = stream['start']
        end = stream['end']
        seconds = stream['seconds']
        bytes = stream['bytes']
        bitrate = stream['bits_per_second']
        jitter = stream['jitter_ms']
        lost = stream['lost_packets']
        total = stream['packets']
        key = f'{date_time}-{start}-{end}'
        data_dict[key] = {
            'interval': f'{start}-{end}',
            'transfer': bytes,
            'bitrate': bitrate,
            'jitter': jitter,
            'lost_total': f'{lost}/{total}'
        }

# Write the data to a CSV file
with open('iperf3_output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date/Time', 'Interval', 'Transfer', 'Bitrate', 'Jitter', 'LOST/TOTAL'])
    for key, data in data_dict.items():
        date_time, interval = key.split('-')[0], data['interval']
        transfer, bitrate, jitter, lost_total = data['transfer'], data['bitrate'], data['jitter'], data['lost_total']
        row = [date_time, interval, transfer, bitrate, jitter, lost_total]
        writer.writerow(row)
