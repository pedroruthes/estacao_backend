# Define os modelos de dados para validação de entrada e serialização de saída
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LocationBase(BaseModel):
    name: str
    lat: float
    lng: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    class Config:
        from_attributes = True

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class ControllerBase(BaseModel):
    location_id: int
    hw_desc: str

class ControllerCreate(ControllerBase):
    pass

class Controller(ControllerBase):
    id: int
    key: str
    enabled: bool
    version: Optional[float]
    class Config:
        from_attributes = True

class ControllerUpdate(BaseModel):
    hw_desc: Optional[str] = None
    enabled: Optional[bool] = None
    location_id: Optional[int] = None
    version: Optional[float] = None

class SensorMeteoSMEBase(BaseModel):
    temperature: float
    humidity: float
    dir_wind: int
    vel_wind: float
    pressure: float
    rain_measure: float

class SensorMeteoSMECreate(SensorMeteoSMEBase):
    pass

class SensorMeteoSME(SensorMeteoSMEBase):
    id: int
    controller_id: int
    time: datetime
    class Config:
        from_attributes = True