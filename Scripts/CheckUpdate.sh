#!/bin/bash

# Check for Patches and Updates 
# Via Cron job, if an update is found
# Apply it and reboot
# Created 11th February 2021 - Jason Brooks

# You will need to modify for your home location
# Ensure you have created the following directories

#mkdir ~/Scripts
#mkdir ~/Scripts/Data
#mkdir ~/Scripts/Data/Logs


MYOUTPUT=/home/pi/Scripts/Data/Logs

# Get Current System TimeStamp...
timestamp=`date '+%y-%m-%d'`

# Get updates
sudo apt update -y > $MYOUTPUT/Update_$timestamp.txt

# Get the list of upgradeable components
apt list --upgradeable > $MYOUTPUT/Avail_$timestamp.txt

# Check the number of lines in the output, assume > 1 line
# We have updates to Apply

if [ ! -f $MYOUTPUT/Avail_$timestamp.txt ]; then
	echo "File not Found!"
	exit
fi
	
count=`wc -l $MYOUTPUT/Avail_$timestamp.txt | cut -d' ' -f1`

if (( $count < 2 ))
then
	exit 
fi

# Apply the updates

sudo apt upgrade -y > $MYOUTPUT/Upgrade_$timestamp.txt
sudo apt full-upgrade -y >> $MYOUTPUT/Upgrade_$timestamp.txt
sudo apt autoremove -y >> $MYOUTPUT/Upgrade_$timestamp.txt
sudo apt clean -y >> $MYOUTPUT/Upgrade_$timestamp.txt

sudo reboot now
