# ZoomJoiner
The aim of this program is to allow the user to automatically login in zoom and start the recording of the screen. 
The idea is that the user doesn't have to be in front of the PC to join and record the meeting. 

The script runs in the bg and checks every minute for an incoming meeting. 
Data for the meeting are provided from a .csv file and is specifically designed for recurrent meeting. 
Listing a meeting for a given day and time will start the join the meeting and start the recording at the same time on that day each week (i.e. Tuesday, 10:00 means that the program will start the process every Tuesday at 10 am).