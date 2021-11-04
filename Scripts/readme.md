# Useful Raspberry Pi Scripts

This folder contained useful Raspberry Pi Scripts I'm using in various projects
They won't necessarily be Production Strength but more for reference code
For you to adapt into your Own Projects

## CheckUpdate.sh

You will need to modify the script for the current user id, and place it into 

  ~/Scripts
  
 Ensure the following Directories are created and available
 
`mkdir ~/Scripts`

`mkdir ~/Scripts/Data`

`mkdir ~/Scripts/Data/Logs`

You will need to update your **crontab** with the following

`16 01 * * * /home/pi/Scripts/CheckUpdate.sh 2>/dev/null &`

Update the time and hour to something more suitable for your system.

The CheckUpdate script will reboot the Pi should an update be found, an updated script 
will be required to prevent this for updates that don't require a reboot.


## CollectMetrics.sh

This script simply collects metric data I'm interested in, currently CPU and GPU Temperature
but can be updated for other metrics, like memory, disk space, IO etc in the future.

Add the following to ***crontab*** 

`0 * * * * /home/pi/Scripts/CollectMetrics.sh &`

`15 * * * * /home/pi/Scripts/CollectMetrics.sh &`

`30 * * * * /home/pi/Scripts/CollectMetrics.sh &`

`45 * * * * /home/pi/Scripts/CollectMetrics.sh &`


## getTempandHumidity.py

This script is a slightly tweaked version of the Freenove Library function
for the DHT11 Sensor

In this example I have connected the DHT11 sensor to GPIO Pin 25
The function will return two values as CSV Humidity and Temperature

i.e. 78%,10.4'C

I've added this to my *CollectMetrics* Scripts to monitor room temperature
and humidty.

It is optional.
