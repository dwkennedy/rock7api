# pydantic json schemas

from typing import List, Union
from pydantic import BaseModel

#class ItemBase(BaseModel):
#    title: str
#    description: Union[str, None] = None


#class ItemCreate(ItemBase):
#    pass


#class Item(ItemBase):
#    id: int
#    owner_id: int

#    class Config:
#        orm_mode = True


class Rock7Message(BaseModel):
    imei: str
    serial: str
    momsn: int
    transmit_time: str
    iridium_latitude: float
    iridium_longitude: float
    iridium_cep: float
    device_type: str
    #JWT: str
    data: str

class WaypointBase(Rock7Message):
    unit_id: int
    state: int
    timestamp: int
    latitude: float
    longitude: float
    altitude: float
    course: float
    speed: float
    pressure: float

class Waypoint(WaypointBase):
    #id: int

    class Config:
        orm_mode = True

