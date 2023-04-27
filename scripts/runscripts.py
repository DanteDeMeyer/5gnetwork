import subprocess

while True:
    # Ask the user to enter a number to choose a script
    script_num = input("Which script do you want to run?\nPress 1 for iperf3.sh\nPress 2 for ping_latency.sh\nPress 3 for quectelRM500q.py\nPress 4 for setupQuectelRM500q.py\nPress 5 for totaliperf3.py\nEnter a number from 1 to 5 (type exit to quit): ")

    # Type exit to break the loop and terminate the program
    if script_num.lower() == 'exit':
        break

    # The entered number will run the script, it will also prompt for a measurement number.
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
            process = ["sudo", "python3", "quectelRM500q.py", "-f", "ATtest.csv", "-m", measurement]
            subprocess.run(process)
        elif script_num == '4':
            subprocess.run(['sudo', 'python3', 'setupQuectelRM500q.py'])
        elif script_num == '5':
            measurement = input("Enter measurement number: ")
            process = ['sudo', 'python3', 'totaliperf3.py', '-f', 'totaliperf.csv', '-m', measurement]
            subprocess.run(process)
    else:
        print("Invalid input. Please enter a number from 1 to 5.")
