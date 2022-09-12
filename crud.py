from sqlalchemy.orm import Session

import models
import schemas


def get_waypoint(db: Session, user_id: int):
    return db.query(models.Waypoint).filter(models.Waypoint.id == waypoint_id).first()


#def get_user_by_email(db: Session, email: str):
#    return db.query(models.User).filter(models.User.email == email).first()


def get_waypoints(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Waypoint).offset(skip).limit(limit).all()


# accept pydantic schema waypoint and store in db model waypoint
#   later I made main.py submit a db model waypoint that is directly
#   inserted into the database
def create_waypoint(db: Session, db_waypoint: models.Waypoint):
    """
    db_waypoint = models.Waypoint(
        unit_id=waypoint.unit_id,
        state=waypoint.state,
        timestamp=waypoint.timestamp,
        latitude=waypoint.latitude,
        longitude=waypoint.longitude,
        altitude=waypoint.altitude,
        course=waypoint.course,
        speed=waypoint.speed,
        pressure=waypoint.pressure,
        imei=waypoint.imei,
        serial=waypoint.serial,
        momsn=waypoint.momsn,
        transmit_time=waypoint.transmit_time,
        iridium_latitude=waypoint.iridium_latitude,
        iridium_longitude=waypoint.iridium_longitude,
        iridium_cep=waypoint.iridium_cep,
        device_type=waypoint.device_type,
        data=waypoint.data)
    """
    db.add(db_waypoint)
    db.commit()
    db.refresh(db_waypoint)
    return db_waypoint

"""
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
"""
