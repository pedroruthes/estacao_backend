# Define as tabelas do banco de dados como classes Python
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, BigInteger, Text, Double
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    lat = Column(Double, nullable=False)
    lng = Column(Double, nullable=False)

    controllers = relationship("Controller", back_populates="location")

class Controller(Base):
    __tablename__ = "controllers"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    hw_desc = Column(Text, nullable=False)
    key = Column(Text, unique=True, nullable=False)
    enabled = Column(Boolean, nullable=False)
    version = Column(Float, nullable=False)

    location = relationship("Location", back_popates="controllers")
    sensors_meteo_sme_data = relationship("SensorMeteoSME", back_populates="controller")

class SensorMeteoSME(Base):
    __tablename__ = "sensors_meteo_sme"
    id = Column(Integer, primary_key=True, index=True)
    controller_id = Column(Integer, ForeignKey("controllers.id"), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    dir_wind = Column(Integer, nullable=False)
    vel_wind = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    rain_measure = Column(Float, nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)

    controller = relationship("Controller", back_populates="sensors_meteo_sme_data")