#!/usr/bin/env python3
########################################################################
# Filename    : FlightStats.py
# Description : Update the LCD Display
# Author      : Jason Brooks www.muckypaws.com
# modification: 7th August 2021
########################################################################
# 
import json
import os
import RPi.GPIO as GPIO
import i2clcd       # pip install i2clcd: https://github.com/WuSiYu/python-i2clcd
                    # https://pypi.org/project/i2clcd/

from time import sleep, strftime
from datetime import datetime
from pathlib import Path

#
# Set Flight Counters 
#
flightMetrics = {
    "flightCount":  0,
    "flightWithName": 0,
    "flightInvalid": 0,
    "flightSeen": 0,
    "flightMax": 0,
    "todaysDate": datetime,
    "max24": 0
}

#
#   Define the InfraRed Motion Sensor Pin
#
sensorPin = 12
ledPin = 11

#
# Using 1602 LCD on i2c Address 0x3F : use i2cdetect -y 1 to validate.
#
# Initialise the LCD Display
#
lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x3F, lcd_width=16)
lcd.init()
lcd.clear()

#
# Get Today's Date
#
def getDateNow():               # get system time
    return datetime.now().strftime('%Y:%m:%d')

#
# Define the Default Values for the Dictionary (Once Initialisation)
#
def defaultValues():
    global flightMetrics
    flightMetrics['flightCount']=0
    flightMetrics['flightWithName']=0
    flightMetrics['flightSeen']=12
    flightMetrics['flightInvalid']=0
    flightMetrics['flightMax']=0
    flightMetrics['max24']=0
    flightMetrics['todaysDate']=getDateNow()
    
#
# Clear Metrics To be Updated by Parsing the aircraft.json file
#
def clearFlightMetrics():
    global flightMetrics
    flightMetrics['flightCount']=0
    flightMetrics['flightWithName']=0
    flightMetrics['flightSeen']=0
    flightMetrics['flightInvalid']=0

#
# Check if Internal Data Available and if so
#   Load it into the dictionary, otherwise, default initialisation
#
def loadData():
    global flightMetrics

    try:
        # initialise default metrics.
        defaultValues()

        # Check if we have an internal data file.
        savedVars = Path("/home/pi/Development/Flight/internalData.json")

        # If a file exists, load the JSON data to the dictionary
        # Also protect against upgrading of the JSON File in the future.
        if savedVars.is_file():
            with open('/home/pi/Development/Flight/internalData.json') as json_file:
                # Load the JSON Data to a Temp Dictionary
                lastKnownData = json.load(json_file)
            if len(lastKnownData) > 0:
                # Copy elements to Global Dictionary (Takes Care in part of versioning)
                for element in lastKnownData:
                    flightMetrics[element] = lastKnownData[element]
    except:
        exit(1)

#
# Helper function, Display Error Message and Quite
#
def quitWithErrorMessage(mess1, mess2):
    lcd.clear()
    lcd.print_line(mess1, line=0)
    lcd.print_line(mess2, line=1)
    exit(1)

#
# Write Internal Dictionary Stats to Local File for Recovery
#
def writeInternalData():
    try:
        with open('/home/pi/Development/Flight/internalData.json','w') as fp:
            json.dump(flightMetrics, fp)
            fp.flush()
            fp.close()
    except:
        quitWithErrorMessage("Failed to Write","Metrics File")

#
# Parse the Flight JSON Data.
#
def parseFlightData():
    global flightMetrics
    #RSA Keys Configured Between the Two Systems
    os.system("scp -C -q pi@flightaware.local:/run/dump1090-fa/aircraft.json /home/pi/Development/Flight/.")

    # Open the JSON File
    try:
        with open('/home/pi/Development/Flight/aircraft.json') as flightStatsFile:
            data = json.load(flightStatsFile)
    except:
        quitWithErrorMessage("Failed to Open","Flight File...")

    #
    # Reset Variables
    #
    clearFlightMetrics()

    for i in data['aircraft']:
        flightMetrics['flightCount']+=1
        data=json.dumps(i, sort_keys=True)
        parsed=json.loads(data)
        if 'seen_pos' in data:
            numSec=parsed['seen_pos']
            if numSec < 60:
                flightMetrics['flightSeen']+=1
        if 'flight' in data:
            flightMetrics['flightWithName']+=1
        else:
            flightMetrics['flightInvalid']+=1
    
    if flightMetrics['flightMax'] < flightMetrics['flightSeen']:
        flightMetrics['flightMax'] = flightMetrics['flightSeen']
        writeInternalData() # Update Internal File Just in Case.
#
# When Exiting the program, Ensure we cleanup the LCD Display.
#
def destroy():
    lcd.clear()
    lcd.set_backlight(False)
    GPIO.cleanup()


#
# Get the current CPU Temperature
#
def get_cpu_temp():     # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.1f}'.format( float(cpu)/1000 ) + '\'C'

#
# Initialisation of the program and sensors.
#
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensorPin, GPIO.IN)
    GPIO.setup(ledPin, GPIO.OUT)
    loadData()

#
#   If someone is present, turn on the LCD Display
#       Otherwise, Switch the LCD Backlight off.
#
def checkPresence():
    if(GPIO.input(sensorPin)) == GPIO.HIGH:
        GPIO.output(ledPin, GPIO.HIGH)
        lcd.set_backlight(True)
    else:
        GPIO.output(ledPin, GPIO.LOW)
        lcd.set_backlight(False)

#
# Main Program Loop
#
def loop():
    while(True):         
        parseFlightData()
        checkPresence()
        lcd.move_cursor(0,0)  # set cursor position
        lcd.print_line( '    CPU: ' + get_cpu_temp() , line=0)# display CPU temperature
        lcd.print_line( 'FLIGHTS: ' + str( flightMetrics['flightSeen']  ) + ',' + str(flightMetrics['flightMax']) + "   " , line=1)
        #lcd.message( get_time_now() )   # display the time

        for timer in range(60):
            checkPresence()
            sleep(0.5)

#
# Main Program...
#
if __name__ == '__main__':
    setup()

    lcd.set_backlight(True)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    
