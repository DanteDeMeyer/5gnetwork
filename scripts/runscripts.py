import subprocess

while True:
    script_num = input("Which script do you want to run?\nPress 1 for iperf3.sh\nPress 2 for ping_latency.sh\nPress 3 for quectelRM500q.py\nPress 4 for setupQuectelRM500q.py\nPress 5 for totaliperf3.py\nEnter a number from 1 to 5 (type exit to quit): ")

    if script_num.lower() == 'exit':
        break

    if script_num in ['1', '2', '3', '4', '5']:
        if script_num == '1':
            measurement = input("Enter measurement number: ")
            process = f"./iperf3.sh 10.45.0.1 iperf3.csv {measurement}"
            subprocess.run([process], shell=True)
        elif script_num == '2':
            measurement = input("Enter measurement number: ")
            process = f"./ping_latency.sh 10.45.0.1 10 ping.csv {measurement}"
            subprocess.run(process, shell=True)
        elif script_num == '3':
            measurement = input("Enter measurement number: ")
            process = f"sudo python3 quectelRM500q.py -f AT.csv -m {measurement}"
            subprocess.run(process, shell=False)
        elif script_num == '4':
            subprocess.run(['sudo python3 setupQuectelRM500q.py'], shell=False)
        elif script_num == '5':
            measurement = input("Enter measurement number: ")
            process = f"sudo python3 totaliperf3.py -f totaliperf.csv -m {measurement}"
            subprocess.run(process, shell=False)
    else:
        print("Invalid input. Please enter a number from 1 to 5.")
