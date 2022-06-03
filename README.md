A small python script to set the WSJT-X maidenhead grid reference with location from GPSD

Developed and tested with Python >= 3.6

Prerequsites
  * pip3 install maidenhead
  * gpsd instance running and getting location from a GPS reciever

How to Run:
  * Clone this Repo
  * python3 wsjtx_grid_from_gpsd.py
  
Notes:
Sometimes this takes a few reads before it returns a Grid, this has to do with the way GPSD returns data, an is expected. This software will listen for packets from WSJT-x and I think that it only sends those packets 
1) when the UDP options are enabled and 
2) when the application starts up.

The way I use this is to run it as a service on my linux laptop so it starts at boot. 
  
The files in the pywsjtx forked from this repo https://github.com/bmo/py-wsjtx
