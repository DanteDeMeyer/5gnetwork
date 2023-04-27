import subprocess
import json
import csv
import os
import argparse
from datetime import datetime, timedelta

# Parse command-line arguments
parser = argparse.ArgumentParser(description='CLI tool for iperf network testing')
parser.add_argument('-m', '--measure')
parser.add_argument('-i', '--ipaddr', default='10.45.0.1', help='serial device path')
parser.add_argument('-l', '--logdir', default='/home/dante/logs', help='logging directory')
parser.add_argument('-f', '--logfile', default='iperf.csv', help='name of the log file (should be .csv)')
args = parser.parse_args()

# Check if the logfile has .csv extension or not
if not args.logfile.endswith('.csv'):
    if '.' in args.logfile:
        file_split = args.logfile.split('.')
        args.logfile = file_split[0] + '.csv'
    else:
        args.logfile += '.csv'

# Check if log directory exists, create it if not
if not os.path.exists(args.logdir):
    os.makedirs(args.logdir)

dirpath = args.logdir
filename= os.path.basename(args.logfile)
path = dirpath + '/' + filename

# Run the iperf3 command and store the JSON data in a variable
result = subprocess.run(['iperf3', '-c', args.ipaddr, '-u', '-b', '100M', '-R', '-J'], stdout=subprocess.PIPE)
data = json.loads(result.stdout)

# Extract the relevant data from the JSON and organize it in a dictionary
data_dict = {}
for i, interval in enumerate(data['intervals']):
    date_time = datetime.strptime(data['start']['timestamp']['time'], '%a, %d %b %Y %H:%M:%S %Z')
    date_time += timedelta(seconds=i)
    protocol = data['start']['test_start']['protocol']
    for stream in interval['streams']:
        start = stream['start']
        end = stream['end']
        seconds = stream['seconds']
        bytes = stream['bytes']
        bitrate = stream['bits_per_second']
        jitter = stream['jitter_ms']
        lost = stream['lost_packets']
        total = stream['packets']
        lost_percent = stream['lost_percent']
        key = f'{start}-{end}'
        data_dict[key] = {
            'measurement': args.measure,
            'date_time': date_time.strftime('%a, %d %b %Y %H:%M:%S %Z'),
            'interval': f'{start}-{end}',
            'transfer': bytes,
            'bitrate': bitrate,
            'jitter': jitter,
            'lost_total': f'{lost}/{total}',
            'lost_percent': lost_percent,
            'protocol': protocol
        }
# Write the data to a CSV file
if os.path.exists(path):
    with open(path, mode='r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames
else:
    headers = list(data_dict.values())[0].keys()
    with open(path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

with open(path, mode='a', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    for data in data_dict.values():
        ordered_data = {k: data[k] for k in headers}
        writer.writerow(ordered_data)
