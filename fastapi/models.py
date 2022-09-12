# database model

from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Waypoint(Base):
    __tablename__ = "waypoints"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer)
    state = Column(Integer)
    timestamp = Column(BigInteger)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    course = Column(Float)
    speed = Column(Float)
    pressure = Column(Float)
    imei = Column(String)
    serial = Column(Integer)
    momsn = Column(Integer)
    transmit_time = Column(String)
    iridium_latitude = Column(Float)
    iridium_longitude = Column(Float)
    iridium_cep = Column(Float)
    device_type = Column(String)
    data = Column(String)

#class Item(Base):
#    __tablename__ = "items"

#    id = Column(Integer, primary_key=True, index=True)
#    title = Column(String, index=True)
#    description = Column(String, index=True)
#    owner_id = Column(Integer, ForeignKey("users.id"))

#    owner = relationship("User", back_populates="items")

