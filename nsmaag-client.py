#!/usr/bin/env python3
#====================================================================================
#
#         FILE: nsmaag-client.py
#
#        USAGE: ./nsmaag-client.py
#
#  DESCRIPTION: This is the main client side program for NSM At A Glance.
#
#      OPTIONS: ---
# REQUIREMENTS: schedule, art, prettytable
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Sean Smith (Student), seasmit2@uat.edu
# ORGANIZATION: NTS370
#      VERSION: 1.0
#      CREATED: 08/22/2018
#     REVISION: ---
#====================================================================================

# Import needed modules and support scripts
import createConfig as create
import editDB as edit
import configparser
import schedule
import sqlite3
import time
import socket
import os
import re
from pathlib import Path
from art import *
from prettytable import from_db_cursor

#------------------------------------------------------------------------
# Use art to create a banner
#------------------------------------------------------------------------
banner = text2art("NSMAAG", "Epic")

#------------------------------------------------------------------------
# Define Variables
#------------------------------------------------------------------------
# Socket Variables
port = 5005

# Path Variables
p = Path('.')

# Database paths
db_path = p / 'databases'
health_db = db_path / 'health.db'

# Config Paths
config_path = p / 'config'
client_config = config_path / 'clientConfig.conf'
server_config = config_path / 'serverConfig.conf'

#------------------------------------------------------------------------
# Create directories if they dont exist
#------------------------------------------------------------------------
if not db_path.exists():
    db_path.mkdir()
    
if not config_path.exists():
    config_path.mkdir()
    
#------------------------------------------------------------------------
# Function to clear the teminal screen regardless of the os being used
#------------------------------------------------------------------------
def clear():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    
    # For Linux/Unix
    else:
        os.system('clear')

#------------------------------------------------------------------------
# Function to Send Database
#------------------------------------------------------------------------
def Send_DB(address, port):
    print("# Sending Database to LED Board")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((address, port))
        file = health_db.open('rb')
        data = file.read(1024)
        while data:
            conn.send(data)
            data = file.read(1024)
        file.close()
    print("# Database Sent!")

#------------------------------------------------------------------------
# Function to clear current count in database
#------------------------------------------------------------------------
def Reset_DB_Count():
    db = sqlite3.connect(str(health_db))
    db_cur = db.cursor()
    
    db_cur.execute("SELECT sign FROM health")
    
    for row in db_cur.fetchall():
        sign = row[0]
        count = 0
        
        db_cur.execute("UPDATE health SET count = ? WHERE sign = ?", (count, sign))
        db.commit()
    
    db_cur.close()
    db.close()
    
#------------------------------------------------------------------------
# Function to search when using rotating logs
#------------------------------------------------------------------------
def Search_Rotating():
    # Connect to Database
    db = sqlite3.connect(str(health_db))
    db_cur = db.cursor()
    
    # Select Data from Database
    db_cur.execute("SELECT * FROM health")
    
    # Itterate through selections
    for row in db_cur.fetchall():
        sign = row[0]
        searchTerm = row[1]
        goodCount = row[2]
        fairCount = row[3]
        count = row[4]
        
        regex = re.compile(searchTerm)
        
        for file in logPath.iterdir():
            if file.suffix == ".log":
                print("Now searching for " + searchTerm + " in " + str(file))
                with open(file, 'r') as log:
                    lines = log.readlines()
                    for line in lines:
                        match = regex.search(line)
                        if match:
                            count += 1
            else:
                pass
            
            db_cur.execute("UPDATE health SET count = ? WHERE sign = ?", (count, sign))
            db.commit()
        
        if count < goodCount:
            health = "GOOD"
        elif count < fairCount:
            health = "FAIR"
        elif count > fairCount:
            health = "BAD"
        
        db_cur.execute("UPDATE health SET health = ? WHERE sign = ?", (health, sign))
        db.commit
        
        db_cur.close()
        db.close()

#------------------------------------------------------------------------
# Function to search when not using rotating logs
#------------------------------------------------------------------------
def Search_NotRotating():
    # Connect to Database
    db = sqlite3.connect(str(health_db))
    db_cur = db.cursor()
    
    # Select Data from Database
    db_cur.execute("SELECT * FROM health")
    
    # Itterate through selections
    for row in db_cur.fetchall():
        sign = row[0]
        searchTerm = row[1]
        goodCount = row[2]
        fairCount = row[3]
        count = 0
        
        regex = re.compile(searchTerm)
        
        for file in logPath.iterdir():
            if file.suffix == ".log":
                print("Now searching for " + searchTerm + " in " + str(file))
                with open(file, 'r') as log:
                    lines = log.readlines()
                    for line in lines:
                        match = regex.search(line)
                        if match:
                            count += 1
            else:
                pass
            
            db_cur.execute("UPDATE health SET count = ? WHERE sign = ?", (count, sign))
            db.commit()
        
        if count < goodCount:
            health = "GOOD"
        elif count < fairCount:
            health = "FAIR"
        elif count > fairCount:
            health = "BAD"
        
        db_cur.execute("UPDATE health SET health = ? WHERE sign = ?", (health, sign))
        db.commit
        
        db_cur.close()
        db.close()

#------------------------------------------------------------------------
# Check for database and create if it doesnt exist
#------------------------------------------------------------------------
if not health_db.exists():
    db = sqlite3.connect(str(health_db))
    db_cur = db.cursor()
    
    # Create table
    db_cur.execute("""CREATE TABLE health
                   (sign INTEGER PRIMARY KEY,
                   search_term TEXT,
                   good_count INT,
                   fair_count INT,
                   count INT,
                   health TEXT)""")
    
    # Close db and cursor
    db_cur.close()
    db.close()

#------------------------------------------------------------------------
# Check to see if a configuration file exists
# If not start process of creating it
#------------------------------------------------------------------------
if not client_config.is_file():
    clear()
    print(banner)
    print("Thank you for choosing NSM At A Glance for your visual NSM needs")
    print("please enter the following information to create the client configuration files.")
    create.Client(client_config)

if not server_config.is_file():
    clear()
    print(banner)
    print("No Server config found please please enter the following informaiton to create one.")
    create.Server(server_config)
    
#------------------------------------------------------------------------
# Show current sign numbers and search terms
#------------------------------------------------------------------------
EDIT_DB = True
while EDIT_DB == True:
    # Connect to database
    db = sqlite3.connect(str(health_db))
    db_cur = db.cursor()
    
    # Select sign, search_term, good_count, and fair_count
    db_cur.execute("SELECT sign, search_term, good_count, fair_count FROM health")
    db_contents = from_db_cursor(db_cur)
    
    db_cur.close()
    db.close()
    
    # Display database contents and accept user input of option    
    clear()
    print(banner)
    print("The following search terms are currently in the database")
    print(db_contents)
    print("\nWhat would you like to do?\n")
    print("1: Continue to program")
    print("2: Add Search Term")
    print("3: Edit Sign Information\n")
    #print("4: Delete Sign\n")
    _selection = input(">> ")
    if _selection == "1":
        EDIT_DB = False
    elif _selection == "2":
        edit.ADD(health_db)
    elif _selection == "3":
        sign_number = input("Which sign would you like to update? ")
        edit.CHANGE(health_db, sign_number)
    #elif _selection == "4":
        #sign_number = input("Which sign would you like to delete? ")
        #edit.DELETE(sign_number)
    else:
        print("Invalid selection please try again")
 
#------------------------------------------------------------------------
# Get config file variables
#------------------------------------------------------------------------
config = configparser.ConfigParser()
config.read(client_config)

# Get Server IP
serverIP = config.get('SERVER', 'IP Address')

# Get Log Path
logs = config.get('LOGS', 'Log Path')
logPath = Path(logs)

# Get rotating info
rotate = config.get('LOGS', 'Rotating')
if rotate.lower() == 'y':
    rotateTime = config.getint('LOGS', 'Rotate Time')
    # Set sleep time based on rotate time
    sleepTime = (rotateTime * 60) - 30
    
#------------------------------------------------------------------------
# Send server config
#------------------------------------------------------------------------
print("# Database and config files set, now sending server config to LED board")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    conn.connect((serverIP, port))
    file = server_config.open('rb')
    data = file.read(1024)
    while data:
        conn.send(data)
        data = file.read(1024)
    file.close()
print("# Server Config sent!")
#------------------------------------------------------------------------
# Set DB count reset schedule
#------------------------------------------------------------------------
schedule.every().day.at("24:59").do(Reset_DB_Count)

#------------------------------------------------------------------------
# Start Main Program Loop
#------------------------------------------------------------------------
try:
    while True:
        # Reset the DB at scheduled time
        schedule.run_pending()
        
        # Search based on rotating or non-rotating logs
        if rotate.lower() == 'y':
            Search_Rotating()
        elif rotate.lower() == 'n':
            Search_NotRotating()

        # Start testing area
        db = sqlite3.connect(str(health_db))
        db_cur = db.cursor()
        
        db_cur.execute("SELECT * FROM health")
        db_contents = from_db_cursor(db_cur)
        
        db_cur.close()
        db.close()
        
        print(db_contents)
        # END TESTING AREA
        
        # Send Database to LED board
        Send_DB(serverIP, port)
        
        # Sleep
        if rotate.lower() == 'y':
            time.sleep(rotateTime)
        elif rotate.lower() == 'n':
            time.sleep(600)

except KeyboardInterrupt:
    tprint("Thank you for using", font='Small Slant')
    print(banner)