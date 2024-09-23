# Created by Jacob Fredriksson
# https://wiresandwi.fi
# https://github.com/wiresandwifi

# Inspired by aaaaaaaaaaaaaaaaaa

import getpass
import netmiko
import csv
from datetime import datetime
#import colorama
from netmiko import ConnectHandler
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
from colorama import Fore, Back, Style, init
import textfsm
import pprint

#import logging
#Enable debug (optional)
#logging.basicConfig(filename='netmiko_logs.txt', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

print(Back.YELLOW)
#print('\n' '.:.:. .:.:. .:.:. .:.:. .:.:.')
print('\n' ' .:.:. Script initiated  .:.:.')
#print('\n' '.:.:. .:.:. .:.:. .:.:. .:.:.')
#print('\n')
print(Style.RESET_ALL)

# Ask user for device credentials (same credentials userd for all devices)
USER = input('Username: ')
PASS = getpass.getpass('Password: ')
# Comment out "EN" below if Enable password is not needed
# ENABLE = getpass.getpass('Enable: ')
print('\n')
print('CONNECTING TO DEVICES... ')
print('\n')


# Default device template
device_template = {
'device_type': 'cisco',
'ip': '1.2.3.4',
'username': USER,
'password': PASS,
'port':22,
# Remove comment below below if Enable password needs to be used
#'secret': ENABLE,
'blocking_timeout': 4 #Default = 8, if timeout problem increase to 16
}

# Keep track of current time for timestamping log files
# Create string variable of current time
current_time = str(datetime.now().replace(microsecond=0))
#string_current_time = str(current)

# Variable to keep track of failed connections to devices 
failed_devices_amount = 0
# List to keep track of device IP addresses 
failed_devices_ip = []
# List to keep track of reason for failure to connect to a device
failed_devices_reason = []

# Open file with devices information (IP and Port)
list_of_devices = csv.DictReader(open('devices_to_configure.csv'))

# Prepare device_template with information from CSV
for row in list_of_devices:
	if (row['port']) == '23':
		device_template['device_type'] = 'cisco_ios_telnet'
		device_template['port'] = '23'
		device_template['ip'] = row['ip']
	else:
		device_template['device_type'] = 'cisco_ios'
		device_template['port'] = '22'
		device_template['ip'] = row['ip']
	try:
		print ('====== Logging IN to device', device_template['ip'],'   ======')
		#Connect to device and send show/config
		net_connect = ConnectHandler(**device_template)
		net_connect.enable()
		#interface_data (prev. "output") = net_connect.send_command_timing('show run', last_read=1, read_timeout=3000)
		print(Fore.GREEN + "====== CONNECTED! ======" + Style.RESET_ALL)
		interface_data = net_connect.send_command('show interfaces switchport', use_textfsm=True)
		
		# Print 
		pprint.pp(interface_data)
		print ('====== Running commands on', device_template['ip'],'   ======')
		#Connect to device and send config
		#net_connect = ConnectHandler(**device_template)
		#net_connect.enable()

		for interface in interface_data:
			if interface['admin_mode'] == 'static access':
       		# Replace this with the actual command you want to run
				print(f"Running command(s) on {interface['interface']}")
				enter_interface = f"interface {interface['interface']}"
				#print(enter_interface)
				#print(enter_interface)
				output1 = net_connect.send_config_set(enter_interface)
				#output2 = net_connect.send_config_from_file('commands_to_send.txt')
				with open('commands_to_send.txt', 'r') as file:
					commands = file.readlines()
					# Strip any newline characters and send the commands within the interface context
					commands = [cmd.strip() for cmd in commands]
				full_command_list = [enter_interface] + commands
				output2 = net_connect.send_config_set(full_command_list)
				#output3 = net_connect.send_config_set("do write mem")
				print(output2)



		#output = net_connect.send_command_timing('show run', last_read=1, read_timeout=3000)
		#output = net_connect.send_config_from_file('commands_to_send.txt')
		#print(Fore.GREEN + "====== CONNECTED! ======" + Style.RESET_ALL)
		#print(output)
		#Save logs in file
		log = open('log_file.txt', 'a')
		log.write('\n')
		log.write(current_time)
		log.write('\n')
		log.write(device_template['ip'])
		log.write('\n')
		log.write(output2)
		log.write('\n')
		print ('====== Saving Configuration on device', device_template['ip'],' ======')
		save_now = net_connect.send_config_set("do write mem")
		net_connect.disconnect()
		print ('====== Logging OUT from device', device_template['ip'],' ======')
		print('\n')



	# Manage and log Authentication failure to device
	except AuthenticationException as err1:
		#print("~" * 15 + str(err2) + "TIMEOUT~" * 15)
		log = open('log_file.txt', 'a')
		log.write('\n')
		log.write(current_time)
		log.write('\n')
		log.write('Unable to access the device (Authentication failed) ')
		log.write(device_template['ip'])
		log.write('\n')
		print(Fore.BLACK + Back.RED + '====== Unable to access device', device_template['ip'],' ======' + Style.RESET_ALL)
		#print(Style.RESET_ALL)
		# Increase failed_devices variable
		failed_devices_amount += 1
		# Add(append) IP address of failed device to list 
		failed_devices_ip.append(device_template['ip'])
		# Convert exception error "e" to a string and save in new variable
		#string_e = str(err1)
		# Save first line of converted exception error (contains failure reason) as variable
		#string_e_line1 = string_e.partition('\n')[0]
		# Add(append) failure reason of failed connection attempt to list
		#failed_devices_reason.append(string_e_line1)
		failed_devices_reason.append("Authentication to device failed.")

	# Manage and log Timeout Exception (device unreachable)
	except NetMikoTimeoutException as err2:
        #print("~" * 15 + str(err2) + "TIMEOUT~" * 15)
		log = open('log_file.txt', 'a')
		log.write('\n')
		log.write(current_time)
		log.write('\n')
		log.write('Unable to access the device (Timeout) ')
		log.write(device_template['ip'])
		log.write('\n')
		print(Fore.BLACK + Back.RED + '====== Unable to access device', device_template['ip'],' ======' + Style.RESET_ALL)
		#print(Style.RESET_ALL)
		# Increase failed_devices variable
		failed_devices_amount += 1
		# Add(append) IP address of failed device to list 
		failed_devices_ip.append(device_template['ip'])
		# Convert exception error "e" to a string and save in new variable
		#string_e = str(err2)
		# Save first line of converted exception error (contains failure reason) as variable
		#string_e_line1 = string_e.partition('\n')[0]
		# Add(append) failure reason of failed connection attempt to list
		#failed_devices_reason.append(string_e_line1)
		failed_devices_reason.append("Connection to device failed.")

		log.close()
	# Manage and log other Exceptions
	except SSHException as e:
		log = open('log_file.txt', 'a')
		log.write('\n')
		log.write(current_time)
		log.write('\n')
		log.write('Unable to access the device (Unknown Error)')
		log.write(device_template['ip'])
		log.write('\n')
		print(Fore.BLACK + Back.RED + '====== Unable to access device', device_template['ip'],' ======' + Style.RESET_ALL)
		#print(Style.RESET_ALL)
		# Increase failed_devices variable
		failed_devices_amount += 1
		# Add(append) IP address of failed device to list 
		failed_devices_ip.append(device_template['ip'])
		# Convert exception error "e" to a string and save in new variable
		string_e = str(e)
		# Save first line of converted exception error (contains failure reason) as variable
		string_e_line1 = string_e.partition('\n')[0]
		# Add(append) failure reason of failed connection attempt to list
		failed_devices_reason.append(string_e_line1)

		log.close()

# If there are failed devices, print the IP address and reason for failure
if failed_devices_amount > 0:
	print('\n')
	print(Fore.BLACK + Back.RED + 'Failed to connect to', failed_devices_amount, 'device(s): ' +  Style.RESET_ALL)
	# Print IP address and Reason for failed devices
	for ip, reason in zip(failed_devices_ip, failed_devices_reason):
			print(ip,'-',reason,)
else:
	pass

#print(Style.RESET_ALL)
print('\n')
print(Back.GREEN)
#print('\n' '.:.:. .:.:. .:.:. .:.:. .:.:.')
print('\n' ' .:.:.  Script finished  .:.:.')
#print('\n' '.:.:. .:.:. .:.:. .:.:. .:.:.')
#print('\n')
print(Style.RESET_ALL)
print('\n')