
# simple python script to read NMEA sentences from a GPSD instance,
# and supply the grid value to wsjtx.

import os
import sys
import threading
from datetime import datetime
import serial
import logging
from gps import *
import time
import maidenhead as mh

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pywsjtx
import pywsjtx.extra.simple_server



IP_ADDRESS = '127.0.0.1'
PORT = 2237


wsjtx_id = None
gps_grid = ""


def read_gpsd():
    new_gps_grid = ""
    gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
    while new_gps_grid == "":
        report = gpsd.next()
        if report['class'] == 'TPV':
            lat = getattr(report,'lat',0.0)
            lon = getattr(report,'lon',0.0)
            print("Lat: " + str(lat) + " Lon: " + str(lon))
        time.sleep(10)
        try:
            new_gps_grid = mh.to_maiden(lat, lon)
            print(" Grid: " + new_gps_grid)
            return new_gps_grid
        except:
            print("No Grid Detected")
    

s = pywsjtx.extra.simple_server.SimpleServer(IP_ADDRESS,PORT)

print("Starting wsjt-x message server")

while True:
    gps_grid == ""
    while gps_grid == "":
        gps_grid = read_gpsd()
	
    (pkt, addr_port) = s.rx_packet()
    if (pkt != None):
        the_packet = pywsjtx.WSJTXPacketClassFactory.from_udp_packet(addr_port, pkt)
        if wsjtx_id is None and (type(the_packet) == pywsjtx.HeartBeatPacket):
            print("wsjtx detected, id is {}".format(the_packet.wsjtx_id))
            print("starting gps monitoring")
            wsjtx_id = the_packet.wsjtx_id

        if type(the_packet) == pywsjtx.StatusPacket:
            if gps_grid != "":
                print("Sending Grid Change to wsjtx-x, old grid:{} new grid: {}".format(the_packet.de_grid, gps_grid))
                grid_change_packet = pywsjtx.LocationChangePacket.Builder(wsjtx_id, "GRID:"+ gps_grid)
                #logging.debug(pywsjtx.PacketUtil.hexdump(grid_change_packet))
                s.send_packet(the_packet.addr_port, grid_change_packet)



