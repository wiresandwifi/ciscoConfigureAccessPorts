[![waw-banner](https://github.com/user-attachments/assets/d8ddb7ea-8d0a-46ab-8e6d-92d2517e93e7)](https://wiresandwi.fi/latest-content)


# Cisco Configure Access Ports
Python script to configure ONLY the Access Ports on any number of Cisco switches.<br> 
Uses a CSV file to import which switches to configure and a simple text file with commands to run.<br><br>

Useful for deploying Access Port specific configurations like VLANs, spanning-tree settings, 802.1x/MAB IBNS 1.0/2.0 policies, device tracking etc.<br>

# Requirements
- Python 3.12.6 (but probably works on earlier releases too).<br>
- See requirements.txt for required modules.<br>

# Features
- Supports switches running both IOS-XE and IOS software. 
- Supports both SSH and Telnet connections.
- Supports both IP and DNS names to connect to network device.
- Includes prompt coloring to make script easier to read.
- Uses ntc-templates to parse show command for finding all access ports.
- Saves the results into a log textfile.

# How To Use
- Install Python.
- Install modules found in requirements.txt.
  - Use "pip install -r requirements.txt" to install all modules automatically.
- Configure CSV file with port/service and IP address/hostname of network devices.
- Configure text file commands_to_send.txt with commands to send to network devices.
- Run configure_accessport.py to start the script.
- Enter username, password (and optionally enable password, see comments in configure_accessport.py).
- Confirm you want to push commands to X devices.
- Commands are executed on network devices one by one and logged to textfile.
- At the end of script, user is informed of failed connections (if any).

# Support
- No support is given for this script.
- Always test the script in a test environment before trying it in a production environment. 
- Use at your own risk.

# Example

Preview of number of devices that will be configured and asks to proceed.
User must type "yes" to confirm script start.<br><br>
![preview1](https://github.com/user-attachments/assets/075f972c-382a-4155-a2e5-d868c534bcfc)


Configuration is automatically saved on the network device after commands are executed.<br><br>
![preview2](https://github.com/user-attachments/assets/b6de6f86-8031-4bb0-bb88-9a7b1ed60963)

Built-in error handling for unreachable devices, wrong credentials, and more.<br><br>
![preview3](https://github.com/user-attachments/assets/aaea0195-efba-4313-aa10-d64dab3c1867)

# Credits
Inspired by/built upon [andreirapuru/netmiko_send_commands](https://github.com/andreirapuru/netmiko_send_commands)<br>

