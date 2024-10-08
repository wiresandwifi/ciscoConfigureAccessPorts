# Created by Jacob Fredriksson
# https://wiresandwi.fi
# https://github.com/wiresandwifi

import getpass
import netmiko
import csv
import textfsm
import pprint
import colorama
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
from colorama import Fore, Back, Style, init, just_fix_windows_console
just_fix_windows_console()

print(Back.YELLOW)
print("\n" " .:.:. Script initiated  .:.:.")
print(Style.RESET_ALL)

# Ask user for device credentials (same credentials are used for all devices)
USER = input("Username: ")
PASS = getpass.getpass("Password: ")
# Un-comment below if Enable password is required to log in to the devices
# ENABLE = getpass.getpass("Enable: ")

# Device template
device_template = {
	"device_type": "cisco",
	"ip": "1.2.3.4",
	"username": USER,
	"password": PASS,
	"port":22,
	# Un-comment below if Enable password is required to log in to the devices
	#"secret": ENABLE,
	# Default = 8, if timeout problem increase to 16
	"blocking_timeout": 4
}

# Keep track of current time for timestamping log files
# Create string variable of current time
current_time = str(datetime.now().replace(microsecond=0))

# Variable to keep track of failed connections to devices 
failed_devices_amount = 0
# List to keep track of device IP addresses 
failed_devices_ip = []
# List to keep track of reason for failure to connect to a device
failed_devices_reason = []

# Open file with devices information (IP and Port)
list_of_devices = csv.DictReader(open("devices_to_configure.csv"))
with open("devices_to_configure.csv") as csv_file:
    list_of_devices = list(csv.DictReader(csv_file))
    line_count = len(list_of_devices)

# Inform user of how many network devices will be configured
print("The following configuration will be pushed to all Access Ports on " + Fore.CYAN + str(line_count) + Style.RESET_ALL + " devices.")
print("")

# Inform user of which commands will be sent to the network devices
f = open('commands_to_send.txt', 'r')
file_contents = f.read()
print(Fore.CYAN + file_contents + Style.RESET_ALL)
print("")
f.close()

# Ask user to confirm to continue
CONTINUE = input("Continue? [yes/no]: ").strip().lower()

if CONTINUE == "yes":
    # Continue with the rest of the script
	print("Continuing the script...")
	print("\n")
	print("Connecting to devices...")
	print("\n")
else:
	# This stops the entire script
    print("Stopping the script.")
    exit()

# Prepare device_template with information from CSV
for row in list_of_devices:
	if (row["port"]) == "23":
		device_template["device_type"] = "cisco_ios_telnet"
		device_template["port"] = "23"
		device_template["ip"] = row["ip"]
	else:
		device_template["device_type"] = "cisco_ios"
		device_template["port"] = "22"
		device_template["ip"] = row["ip"]
	try:
		# Connect to device and send initial show command to gather interface data
		# Textfsm template from Network-to-Code (included in NetMiko) is used to parse output from this specific show command
		# The template will create a list of dictionaries to be used later to match access ports
		print ("====== Logging IN to device", device_template["ip"],"   ======")
		net_connect = ConnectHandler(**device_template)
		net_connect.enable()
		print(Fore.GREEN + "====== CONNECTED! ======" + Style.RESET_ALL)
		interface_data = net_connect.send_command("show interfaces switchport", use_textfsm=True)
		
		# Print output from show interfaces switchport using pprint for better visibility
		# Un-comment line below to see parsed result of "show interfaces switchport" for debugging purposes
		#pprint.pp(interface_data)
		# Inform that configuration will be sent to the device
		print("====== Running commands on", device_template["ip"], "   ======")
		# Open log file and append append timestamp and device IP/hostname
		log = open("log_file.txt", "a")
		log.write("\n")
		log.write("\n")
		log.write("Time: " + current_time)
		log.write("\n")
		log.write("Device: " + device_template["ip"])
		log.write("\n")
		log.write("Commands executed:")
		log.write("\n")
		log.close()

		# For-loop to configure interfaces matching "admin_mode" == "static access", meaning they are access ports
		for interface in interface_data:
			if interface["admin_mode"] == "static access":
       		# Enter the specific Access Port before executing commands from CSV
				print(f"Running command(s) on {interface["interface"]}")
				enter_interface = f"interface {interface["interface"]}"
				output_enter_interface = net_connect.send_config_set(enter_interface)
				# Open CSV file "commands_to_send.txt" which contains the interface commands to send
				with open("commands_to_send.txt", "r") as file:
					commands = file.readlines()
					# Strip any newline characters and send the commands within the interface context
					commands = [cmd.strip() for cmd in commands]
				full_command_list = [enter_interface] + commands
				output_full_command_list = net_connect.send_config_set(full_command_list)
				print(output_full_command_list)

				# Open log file and append commands that have been run
				log = open("log_file.txt", "a")
				log.write("\n")
				log.write(output_full_command_list)
				log.write("\n")
				log.close()
		
		# Send "do write mem" to device to save configuration
		print(Back.CYAN + Fore.BLACK + "====== Finished! Saving Configuration on device", device_template["ip"], " ======" + Style.RESET_ALL)		
		save_now = net_connect.send_config_set("do write mem")
		log = open("log_file.txt", "a")
		log.write("====== Saving configuration ======")
		print("\n")
		log.write(save_now)
		# Disconnect from device
		net_connect.disconnect()
		# Close log file
		log.close()
		
		print ("====== Logging OUT from device", device_template["ip"]," ======")
		print("\n")

	# Manage and log authentication failures to device
	except AuthenticationException as err1:
		log = open("log_file.txt", "a")
		log.write("\n")
		log.write("\n")
		log.write("Time: " + current_time)
		log.write("\n")
		log.write("Device: " + device_template["ip"])
		log.write("\n")
		log.write("Unable to access the device (Authentication failed). ")
		log.write("\n")
		print(Fore.BLACK + Back.RED + "====== Unable to access device", device_template["ip"]," ======" + Style.RESET_ALL)
		# Increase failed_devices variable by 1
		failed_devices_amount += 1
		# Add(append) IP address of failed device to list "failed_devices_ip"
		failed_devices_ip.append(device_template["ip"])
		# Convert exception error "e" to a string and save in new variable
		# Save first line of converted exception error (contains failure reason) as variable
		# Add(append) failure reason of failed connection attempt to list "failed_devices_reason"
		failed_devices_reason.append("Authentication to device failed.")
		log.close()

	# Manage and log Timeout Exception (device unreachable)
	except NetMikoTimeoutException as err2:
		log = open("log_file.txt", "a")
		log.write("\n")
		log.write("\n")
		log.write("Time: " + current_time)
		log.write("\n")
		log.write("Device: " + device_template["ip"])
		log.write("\n")
		log.write("Unable to access the device (Timeout). ")
		log.write("\n")
		print(Fore.BLACK + Back.RED + "====== Unable to access device", device_template["ip"], " ======" + Style.RESET_ALL)
		
		# Increase failed_devices variable
		failed_devices_amount += 1
		# Add(append) IP address of failed device to list 
		failed_devices_ip.append(device_template["ip"])
		# Add(append) failure reason of failed connection attempt to list
		failed_devices_reason.append("Connection to device failed.")
		log.close()

	# Manage and log other Exceptions
	except SSHException as e:
		log = open("log_file.txt", "a")
		log.write("\n")
		log.write("Time: " + current_time)
		log.write("\n")
		log.write("Device: " + device_template["ip"])
		log.write("\n")
		log.write("Unable to access the device (Unknown Error). ")
		log.write("\n")
		print(Fore.BLACK + Back.RED + "====== Unable to access device", device_template["ip"]," ======" + Style.RESET_ALL)
		# Increase failed_devices variable by 1
		failed_devices_amount += 1
		# Add(append) IP address of failed device to list 
		failed_devices_ip.append(device_template["ip"])
		# Add(append) reason of failed connection attempt to list
		failed_devices_reason.append("Connection failed (Unknown Error).")
		log.close()

# If there are failed devices, print the IP address and reason for failure for those devices
if failed_devices_amount > 0:
	print("\n")
	print(Fore.BLACK + Back.RED + "Failed to connect to", failed_devices_amount, "device(s): " +  Style.RESET_ALL)
	# Print IP address and Reason for failed devices
	for ip, reason in zip(failed_devices_ip, failed_devices_reason):
		print(ip,"-",reason,)
else:
	pass

print("\n")
print(Back.GREEN)
print("\n" " .:.:.  Script finished  .:.:.")
print(Style.RESET_ALL)
print("\n")
