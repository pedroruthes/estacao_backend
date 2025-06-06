# Contém as funções de interação com o banco de dados
from sqlalchemy.orm import Session
from app import models, schemas
import secrets # Para gerar tokens de API
from datetime import datetime, timezone

def update_model_from_schema(model, schema):
    for field, value in schema.dict(exclude_unset=True).items():
        setattr(model, field, value)
    return model

# Funções CRUD para Locations
def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def update_location(db: Session, db_location: models.Location, location_update: schemas.LocationUpdate):
    updated_db_location = update_model_from_schema(db_location, location_update)
    db.add(updated_db_location)
    db.commit()
    db.refresh(updated_db_location)
    return updated_db_location


# Funções CRUD para Controllers
def get_controller(db: Session, controller_id: int):
    return db.query(models.Controller).filter(models.Controller.id == controller_id).first()

def get_controller_by_key(db: Session, key: str):
    return db.query(models.Controller).filter(models.Controller.key == key).first()

def get_controllers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Controller).offset(skip).limit(limit).all()

def create_controller(db: Session, controller: schemas.ControllerCreate):
    api_key = secrets.token_urlsafe(32)
    db_controller = models.Controller(**controller.model_dump(), key=api_key)
    db.add(db_controller)
    db.commit()
    db.refresh(db_controller)
    return db_controller

def update_controller(db: Session, controller_id: int, controller_update: schemas.ControllerUpdate):
    db_controller = get_controller(db, controller_id)
    if db_controller:
        update_data = controller_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_controller, key, value)
        
        db.add(db_controller)
        db.commit()
        db.refresh(db_controller)
    return db_controller

# Funções CRUD para Sensors
def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

def update_sensor(db: Session, sensor_id: int, sensor_update: schemas.SensorUpdate):
    db_sensor = get_sensor(db, sensor_id)
    if db_sensor:
        update_data = sensor_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sensor, key, value)
        
        db.add(db_sensor)
        db.commit()
        db.refresh(db_sensor)
    return db_sensor

def delete_sensor(db: Session, sensor_id: int):
    db_sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

    if db_sensor:
        sensor_to_return = schemas.Sensor.model_validate(db_sensor)
        db.delete(db_sensor)
        db.commit()
        return sensor_to_return
    
    return None

# Funções CRUD para SensorMeteoSME
def create_sensor_meteo_sme_data(db: Session, data: schemas.SensorMeteoSMECreate, controller_id: int):
    db_data = models.SensorMeteoSME(**data.model_dump(), controller_id=controller_id, time=datetime.now(timezone.utc))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_sensor_meteo_sme_data_by_controller(
    db: Session, controller_id: int, skip: int = 0, limit: int = 100
):
    return db.query(models.SensorMeteoSME).filter(
        models.SensorMeteoSME.controller_id == controller_id
    ).order_by(models.SensorMeteoSME.time.desc()).offset(skip).limit(limit).all()

def get_sensor_meteo_sme_data_by_controller_and_time_range(
    db: Session,
    controller_id: int,
    start_time: datetime,
    end_time: datetime,
    skip: int = 0,
    limit: int = 100
):
    return db.query(models.SensorMeteoSME).filter(
        models.SensorMeteoSME.controller_id == controller_id,
        models.SensorMeteoSME.time >= start_time,
        models.SensorMeteoSME.time <= end_time
    ).order_by(models.SensorMeteoSME.time.desc()).offset(skip).limit(limit).all()