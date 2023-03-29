import csv
response_dict = { 'Name': ['X','y','z'],
      		  'Number': [21,22,23,24,25],
		  'number2': [71,72,73,77]
                }
with open('datelog.csv','w',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(response_dict.keys())
    for iteration in range(len(response_dict.keys())):
        writer.writerow([val[iteration] for val in response_dict.values()])
