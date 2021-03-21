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
