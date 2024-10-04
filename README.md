# Cisco Configure Access Ports
Python script to configure ONLY access ports on any number of Cisco switches. 

# Requirements
Python 3.12.6 (but might work on earlier releases too)
See requirements.txt for needed modules

# Features
Support switches running both IOS-XE and IOS software. 
Support both SSH and Telnet connections.
Supports both IP and DNS names to connect to switches.
Includes prompt coloring to make script easier to read.
Use ntc-templates to parse show command for finding all access ports
Save results into a log textfile.

# How To Use
Install Python
Install modules found in requirements.txt
Configure CSV file with port/service and IP/hostname of network device

# Example

Preview of number of devices that will be configured and asks to proceed
![preview1](https://github.com/user-attachments/assets/ce6e073e-10f9-490a-b96d-c22790c9fa10)

Configuration is automatically saved on the network device.
![preview2](https://github.com/user-attachments/assets/b6de6f86-8031-4bb0-bb88-9a7b1ed60963)

Built-in error handling:
![preview3](https://github.com/user-attachments/assets/aaea0195-efba-4313-aa10-d64dab3c1867)
