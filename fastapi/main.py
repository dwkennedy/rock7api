#__package__ = "/home/doug/fastapi/test"

from fastapi import FastAPI, Request, Depends, HTTPException
from typing import Union, List
from pydantic import BaseModel, ValidationError
from struct import *
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# take Rock7Message delivered by ground station, insert into waypoint DB
#@app.post("/waypoint", response_model=schemas.Waypoint)
@app.post("/waypoint", response_model=None)
def add_waypoint(rock7: schemas.Rock7Message, db: Session = Depends(get_db)):

    # verify hex encoded data is even length (two bytes per hex char)
    #    then we pad and trim to length to match format
    #    if we change message format in tracker firmware we'll have
    #    to update this code to match
    #    the "<" char in format is little-endian, no alignment
    #    as the AVR doesn't pad/align bytes in a structure
    beacon_format = "< HBBBBBBBllhhhL"
    foo = bytearray.fromhex(rock7.data) + bytearray(27)
    foo = foo[0:27]
    #print ("foo: ", foo.hex())

    (unit_id, state, second, minute, hour, day, month, year,
        latitude,longitude,altitude,course,speed,
        pressure) = unpack(beacon_format,foo)
    # fix integer scaling
    latitude /= 1000000
    longitude /= 1000000
    course /= 10
    speed /= 10
    # build unix timestamp from received date/time
    try:
        dt = datetime( year=(year+2000), month=month, day=day,
                       hour=hour, minute=minute, second=second).timestamp()
    except ValueError:
        dt = datetime.fromtimestamp(0).timestamp()

    # map rock7 raw mesage and fields decoded from hex data to
    #   a database model
    waypoint = dict()
    waypoint['unit_id'] = unit_id
    waypoint['state'] = state
    waypoint['timestamp'] = dt
    waypoint['latitude'] = latitude
    waypoint['longitude'] = longitude
    waypoint['altitude'] = altitude
    waypoint['course'] = course
    waypoint['speed'] = speed
    waypoint['pressure'] = pressure
    waypoint['imei'] = rock7.imei
    waypoint['serial'] = rock7.serial
    waypoint['momsn'] = rock7.momsn
    waypoint['transmit_time'] = rock7.transmit_time
    waypoint['iridium_latitude'] = rock7.iridium_latitude
    waypoint['iridium_longitude'] = rock7.iridium_longitude
    waypoint['iridium_cep'] = rock7.iridium_cep
    waypoint['device_type'] = rock7.device_type
    waypoint['data'] = rock7.data
    #print ("waypoint: ", waypoint)
    try:
        db_waypoint = models.Waypoint ( **waypoint )
    except ValidationError as e:
        print(e.json())

    # insert the database model into the database
    data = crud.create_waypoint(db=db, db_waypoint=db_waypoint)

    return None

"""
struct sat_message {
  uint16_t unit_id; // (0xFFFF = unset)
  uint8_t state;    // 0=prelaunch, 3=flight, etc
  uint8_t second;   // 0-59
  uint8_t minute;   // 0-59
  uint8_t hour;     // 0-23
  uint8_t day;      // 1-31
  uint8_t month;    // 1-12
  uint8_t year;     //(2000 plus 0-255)
  int32_t latitude;   // N, millionths of degrees
  int32_t longitude;  // E, millionths of degrees
  int16_t altitude;    // up to 32767 meters, 107,503 ft
  int16_t course;   // 10ths of a degree
  int16_t speed;    // 10ths of m/s
  uint32_t pressure;   // Pa 0-172369
  //int16_t temp;      // in tenths of deg C
  //iint16_t humidity; // in tenths of percent 0-1000
};
"""


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.Rock7Message):
    return {"imei": item.imei, "serial": item.serial, "data": item.data }

@app.post("/test")
async def test_item(info: Request):
    req_info = await info.json()
    print(req_info)
    return {
            "status" : "SUCCESS",
            "data" : req_info
    }

"""
sample request

{'momsn': 85, 'data': '546865726520617265203130207479706573206f662070656f706c652077686f20756e6465727374616e642062696e617279', 'serial': 8536, 'iridium_latitude': 42.7463, 'iridium_cep': 123.0, 'JWT': 'eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJSb2NrIDciLCJpYXQiOjE2NjI3NTkxMzYsImRhdGEiOiI1NDY4NjU3MjY1MjA2MTcyNjUyMDMxMzAyMDc0Nzk3MDY1NzMyMDZmNjYyMDcwNjU2ZjcwNmM2NTIwNzc2ODZmMjA3NTZlNjQ2NTcyNzM3NDYxNmU2NDIwNjI2OTZlNjE3Mjc5IiwiZGV2aWNlX3R5cGUiOiJST0NLQkxPQ0siLCJpbWVpIjoiMzAwMjM0MDYxNDg2MzYwIiwiaXJpZGl1bV9jZXAiOiIxMjMuMCIsImlyaWRpdW1fbGF0aXR1ZGUiOiI0Mi43NDYzIiwiaXJpZGl1bV9sb25naXR1ZGUiOiIxNDMuMDk2MyIsIm1vbXNuIjoiODUiLCJzZXJpYWwiOiI4NTM2IiwidHJhbnNtaXRfdGltZSI6IjIyLTA5LTA5IDIxOjMyOjEzIn0.kgZodZKI70jCZ5hQGwZyI1Z0aQHu7GDzB1MX_ZT0eM6V77JGvoGzMMuyuvXmuu0Eb7Y1CH19PkegHCxoi_EVNe8-A5eATsuv7u_U2nw-GDOo4712CF79OpJB-8egT7Rgom_rnfb8da5ynHd3bS6SGxbx6n6JMKqKOZ6t_I-HfSQk_AxXzQNy0WKQZRFYbskKwTdD_hkZi-tNicdYVbvflqqZqJcixKXuZyIL9xyku2UwY3i_mIy4Ao0MgUeXMlIQLXW-U5fWHNibaQrCMGP0HRFuKcQ-aGKbrTfcLpnpv3S6T1682oaQVprj27M0LfNUchy8wcQmU6oLWZSPnHnigw', 'imei': '300234061486360', 'device_type': 'ROCKBLOCK', 'transmit_time': '22-09-09 21:32:13', 'iridium_longitude': 143.0963}
"""
