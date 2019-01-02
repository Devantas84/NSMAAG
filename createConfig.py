#!/usr/bin/env python3
#====================================================================================
#
#         FILE: ceateMenu.py
#
#        USAGE: N/A called only
#
#  DESCRIPTION: Script containing the menu for creating config files
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Sean Smith (Student), seasmit2@uat.edu
# ORGANIZATION: NTS370
#      VERSION: 1.0
#      CREATED: 08/22/2018
#     REVISION: ---
#====================================================================================

# Import needed modules and scripts
import configparser
import os

#------------------------------------------------------------------------
# Function to create / edit client config
#------------------------------------------------------------------------
def Client(filePath):
    # Create net configparser instance for client
    client = configparser.ConfigParser()
    
    # Add sections to config
    client.add_section('SERVER')
    client.add_section('LOGS')
    
    # Get User Input
    serverIP = input("Server IP Address: ")
        
    print("\n"
          "Please supply the full path to the log files as shown in the following examples."
          "\n  Windows: C:/path/to/log/files/"
          "\n  Linux: /path/to/log/files/"
          "\n")
    
    logPath = input("Full path to log files: ")
    
    print("\n"
          "Do the logs rotate? (i.e. The logs reset after a set period of time)")
    rotate = input("[Y/N] > ")
    
    if rotate.lower() == 'y':
        client.set('LOGS', 'Rotating', rotate)
        rotateTime = input("How often, in minutes, do they rotate? ")
        client.set("LOGS", 'Rotate Time', rotateTime)
    else:
        client.set('LOGS', 'Rotating', rotate)
    
    # Set user supplied values
    client.set('SERVER', 'IP Address', serverIP)
    client.set('LOGS', 'Log Path', logPath)
    
    # Write the config file
    with open(filePath, 'w') as clientConfig:
        client.write(clientConfig)

#------------------------------------------------------------------------
# Function to create / edit server config
#------------------------------------------------------------------------
def Server(filePath):
    # Create new configparser instance for server
    server = configparser.ConfigParser()
    
    # Add LED Section to config
    server.add_section('LED')
    
    # Get User input
    _num_leds_per_sign = input("Number of LED's per sign: ")
    _num_signs = input("Number of Signs: ")
    
    # Set user supplied values
    server.set('LED', 'num_per_sign', _num_leds_per_sign)
    server.set('LED', 'num_signs', _num_signs)
    
    # Write the config file
    with open(filePath, 'w') as serverConfig:
        server.write(serverConfig)

if __name__ == "__main__":
    print("Please use client.py to start the program!")