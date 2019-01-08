#!/usr/bin/env python3
#====================================================================================
#
#         FILE: nsmaag.py
#
#        USAGE:   
#
#  DESCRIPTION: 
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Sean Smith (Student), seasmit2@uat.edu
# ORGANIZATION: NTS370
#      VERSION: 1.0
#      CREATED: 11/20/2018
#     REVISION: ---
#====================================================================================

#------------------------------------------------------------------------
# Import Modules
#------------------------------------------------------------------------
import board
import neopixel
import socket
import sqlite3
import configparser
import os

#------------------------------------------------------------------------
# Set Variables
#------------------------------------------------------------------------
# Socket Variables
_host = ""
_port = 5005

# LED's
_pixel_pin = board.D18

#------------------------------------------------------------------------
# Define Functions
#------------------------------------------------------------------------
def recv_db():
    print("## Waiting to recieve database")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((_host, _port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print("# Recueved connection from " + str(conn))
            print("# Saving database now")
            with open("health.db", 'wb') as db:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    db.write(data)

def update_sign(_start, _end, color):
    for i in range(_start, _end):
        pixels[i] = color
        pixels.show()

#------------------------------------------------------------------------
# Wait for config file if it does not exist
#------------------------------------------------------------------------
if not os.path.isfile('serverconfig.conf'):
    print("## Waiting for server config File")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((_host, _port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            with open('serverconfig.conf', 'wb') as conf:
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    conf.write(data)

#------------------------------------------------------------------------
# Initalize LEDs
#------------------------------------------------------------------------
print("# Server config file recieved, processing now")

config = configparser.ConfigParser()
config.read('serverconfig.conf')

# Create vaiables from config information
num_led_per_sign = config.getint('LED', 'num_per_sign')
print(type(num_led_per_sign))
print("Number of LED's per sign = "+str(num_led_per_sign))
num_signs = config.getint('LED', 'num_signs')
print(type(num_signs))
print("Number of Signs = "+str(num_signs))
num_leds = num_led_per_sign * num_signs
print(type(num_leds))
print("Total Number of LED's = "+str(num_leds))

# Create Pixel Object
pixels = neopixel.NeoPixel(_pixel_pin, num_leds, auto_write=False)

# Set all LED's to green
pixels.fill((0, 255, 0))
pixels.show()

#------------------------------------------------------------------------
# Start Main Program Cycle
#------------------------------------------------------------------------
try:
    while True:
        # Recieve Database File
        recv_db()
        print("# Database recieved setting LEDs now")
        
        # Connect to database and create cursor
        db = sqlite3.connect('health.db')
        db_cur = db.cursor()
        
        # Select sign number and health value from database
        db_cur.execute("SELECT sign, health FROM health")
        
        # Itterate through selections
        for row in db_cur.fetchall():
            sign_number = row[0]
            sign_health = row[1]
            
            # Calculate Starting and Ending pixel
            ending_led = sign_number * num_led_per_sign
            starting_led = ending_led - num_led_per_sign
            
            # Change LED color for signs
            if sign_health == "GOOD":
                update_sign(starting_led, ending_led, (0, 255, 0))
            elif sign_health == "FAIR":
                update_sign(starting_led, ending_led, (255, 255, 0))
            elif sign_health == "BAD":
                update_sign(starting_led, ending_led, (255, 0, 0))
        
        # Close db connection and cursor
        db_cur.close()
        db.close()
        
        print("# LEDs set!")

# Clear LEDs on Keyboard Interrupt
except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
    os.remove("health.db")
    os.remove("serverconfig.conf")
    
