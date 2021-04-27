#!/bin/bash

# Data Collection Script for system metrics
# V1.00 - Jason Brooks - 11th Feb 2021

# Get Current System TimeStamp...
timestamp=`date '+%y-%m-%d %H:%M:%S'`

# Get CPU and System Temperature
cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
cpuTemp1=$(($cpuTemp0/1000))
cpuTemp2=$(($cpuTemp0/100))
cpuTempM=$(($cpuTemp2 % $cpuTemp1))

# Calculate Human Readable Temperatures
CPUTemp=$cpuTemp1"."$cpuTempM"'C"
GPUTemp=$(/opt/vc/bin/vcgencmd measure_temp | cut -d= -f2)

# Write to CSV File
echo "`hostname` , $timestamp , $CPUTemp , $GPUTemp" >> /home/pi/Scripts/Data/Temperature.csv
