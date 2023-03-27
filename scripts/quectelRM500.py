#!/usr/bin/env python3

from attila.atre import ATRuntimeEnvironment
from attila.exceptions import ATREUninitializedError, ATRuntimeError, ATScriptNotFound, ATScriptSyntaxError, ATSerialPortError

# Configuration
device = '/dev/ttyUSB2'
baud_rate = 115200
timeout = 2
line_break = '\r\n'
command = "AT"

# Create ATRuntimeEnvironment object
atrunenv = ATRuntimeEnvironment(True)

# Configure communicator
atrunenv.configure_communicator(device, baud_rate, timeout, line_break)

# Open serial port
atrunenv.open_serial()

# Add command to the session
response = atrunenv.exec('AT+CIMI')
print(response.full_response)
response = atrunenv.exec('AT+cfun=0')
print(response.full_response)
response = atrunenv.exec('AT+cfun=1')
print(response.full_response)
response = atrunenv.exec('AT+CGDCONT=1,"IPV4V6","oai"')
print(response.full_response)
exit(0)
atrunenv.add_command('AT')

# Execute commands
try:
    response_list = atrunenv.run()
    for response in response_list:
        print(response)
except ATRuntimeError as e:
    print("Command failed with error:", e)

# Close serial port
atrunenv.close_serial()
