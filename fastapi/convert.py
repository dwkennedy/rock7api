#!/usr/bin/python3

# this is a test of unpacking a binary string into various
#   structure members in python (packed by an AVR C program)

from datetime import datetime
from struct import *

datahex = "0000001D041107091664B91902D87531FA6E01E20901000F7E0100"
# data = "0000 00 1D 04 11 07 09 16 64B91902 D87531FA 6E01 E209 0100 0F7E0100"
#  2022-09-07 17:04:29
#db_waypoint:  {'unit_id': 0, 'state': 0, 'timestamp': 1662570269, 'latitude': 1080865052526997242, 'longitude': 382, 'altitude': 0, 'course': 0, 'speed': 0, 'pressure': 0, 'id': 123}

data = bytes.fromhex(datahex)


beacon_format = "< HBBBBBBBllhhhL"
foo = bytearray.fromhex(datahex) + bytearray(54)
foo = foo[0:27]
print ("foo: ", foo.hex())

(unit_id, state, second, minute, hour, day, month, year,
    latitude,longitude,altitude,course,speed,
    pressure) = unpack(beacon_format,foo)
# build unix timestamp from received date/time
dt = datetime( year=(year+2000), month=month, day=day,
         hour=hour, minute=minute, second=second)
print(dt)
print(dt.timestamp())

db_waypoint = dict()
db_waypoint['unit_id'] = unit_id
db_waypoint['state'] = state
db_waypoint['timestamp'] = int(dt.timestamp())
db_waypoint['latitude'] = latitude
db_waypoint['longitude'] = longitude
db_waypoint['altitude'] = altitude
db_waypoint['course'] = course
db_waypoint['speed'] = speed
db_waypoint['pressure'] = pressure
db_waypoint['id'] = 123
print ("db_waypoint: ", db_waypoint)



