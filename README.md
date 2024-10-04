# Cisco Configure Access Ports
Python script to configure ONLY access ports on any number of Cisco switches.<br> 
Uses a CSV file to import which switches to configure and a simple text file with commands to run.<br>

# Requirements
- Python 3.12.6 (but might work on earlier releases too)<br>
- See requirements.txt for needed modules<br>

# Features
- Supports switches running both IOS-XE and IOS software. 
- Supports both SSH and Telnet connections.
- Supports both IP and DNS names to connect to network device.
- Includes prompt coloring to make script easier to read.
- Uses ntc-templates to parse show command for finding all access ports.
- Saves results into a log textfile.

# How To Use
- Install Python.
- Install modules found in requirements.txt.
  - Use "pip install -r requirements.txt" to install all modules automatically.
- Configure CSV file with port/service and IP/hostname of network devices.
- Configure text file commands_to_send.txt with commands to send to network devices.
- Run configure_accessport.py to start the script.
- Enter username, password (and optionally enable password, see comments in configure_accessport.py).
- Confirm you want to push commands to X devices.
- Commands are executed on network devices one by one and logged to textfile.
- At the end of script, user is informed of failed connections.

# Support
- No support is given for this script.
- Always test the script in a test environment before trying it in a production environment. 
- Use at your own risk.

# Example

Preview of number of devices that will be configured and asks to proceed.
User must type "yes" to confirm script start.<br>
![preview1](https://github.com/user-attachments/assets/ce6e073e-10f9-490a-b96d-c22790c9fa10)

Configuration is automatically saved on the network device after commands are executed.<br>
![preview2](https://github.com/user-attachments/assets/b6de6f86-8031-4bb0-bb88-9a7b1ed60963)

Built-in error handling for unreachable devices, wrong credentials, and more.<br>
![preview3](https://github.com/user-attachments/assets/aaea0195-efba-4313-aa10-d64dab3c1867)



