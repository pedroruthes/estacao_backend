from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, BigInteger, Text, Double
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timedelta, timezone

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    lat = Column(Double, nullable=False)
    lng = Column(Double, nullable=False)

    controllers = relationship("Controller", back_populates="location")
    persons = relationship("PersonLocation", back_populates="location")

class Controller(Base):
    __tablename__ = "controllers"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    hw_desc = Column(Text, nullable=False)
    key = Column(Text, unique=True, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    version = Column(Float, nullable=True)

    location = relationship("Location", back_populates="controllers")
    sensors_meteo_sme_data = relationship("SensorMeteoSME", back_populates="controller")
    sensors = relationship("SensorController", back_populates="controller")

class SensorMeteoSME(Base):
    __tablename__ = "sensors_meteo_sme"
    id = Column(Integer, primary_key=True, index=True)
    controller_id = Column(Integer, ForeignKey("controllers.id"), nullable=False, index=True)
    temperature = Column(Float, nullable=True) 
    humidity = Column(Float, nullable=True)    
    dir_wind = Column(Integer, nullable=True)  
    vel_wind = Column(Float, nullable=True)    
    pressure = Column(Integer, nullable=True) 
    rain_measure = Column(Float, nullable=True) 
    time = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    controller = relationship("Controller", back_populates="sensors_meteo_sme_data")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    persons = relationship("Person", back_populates="profile")

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    persons = relationship("Person", back_populates="position")

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False, index=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False, index=True)

    profile = relationship("Profile", back_populates="persons")
    position = relationship("Position", back_populates="persons")
    locations = relationship("PersonLocation", back_populates="person")
    forgot_passwords = relationship("ForgotPassword", back_populates="person")
    log_events = relationship("LogEvent", back_populates="person")

class PersonLocation(Base):
    __tablename__ = "persons_locations"
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), primary_key=True)

    location = relationship("Location", back_populates="persons")
    person = relationship("Person", back_populates="locations")

class ForgotPassword(Base):
    __tablename__ = "forgot_passwords"
    id = Column(Integer, primary_key=True, index=True)
    recovery_code = Column(Integer, nullable=False)
    expire_in = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=15))
    used = Column(Boolean, nullable=False, default=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False, index=True)

    person = relationship("Person", back_populates="forgot_passwords")

class LogEvent(Base):
    __tablename__ = "log_events"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False, index=True)

    person = relationship("Person", back_populates="log_events")

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)

    controllers = relationship("SensorController", back_populates="sensor")

class SensorController(Base):
    __tablename__ = "sensors_controllers"
    sensor_id = Column(Integer, ForeignKey("sensors.id"), primary_key=True)
    controller_id = Column(Integer, ForeignKey("controllers.id"), primary_key=True)

    sensor = relationship("Sensor", back_populates="controllers")
    controller = relationship("Controller", back_populates="sensors")