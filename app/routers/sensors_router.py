from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/sensors", tags=["Sensores"])

# Cria um novo sensor
@router.post("/", response_model=schemas.Sensor)
def create_sensor(
    sensor: schemas.SensorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_sensor(db=db, sensor=sensor)

# Retorna todos os sensores cadastrados, com paginação opcional
@router.get("/", response_model=List[schemas.Sensor])
def read_sensors(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    sensors = crud.get_sensors(db, skip=skip, limit=limit)
    return sensors

# Atualiza um sensor existente pelo ID
@router.patch("/{sensor_id}", response_model=schemas.Sensor)
def update_sensor(
    sensor_id: int,
    sensor: schemas.SensorUpdate,
    db: Session = Depends(get_db)
):
    db_controller = crud.get_sensor(db, sensor_id=sensor_id)
    if db_controller is None:
        raise HTTPException(status_code=404, detail="Controlador não encontrado")
    
    update_data = sensor.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")

    updated_sensor = crud.update_sensor(db=db, sensor_id=sensor_id, sensor_update=sensor)
    return updated_sensor

# Deletar um sensor pelo ID
@router.delete("/{sensor_id}", response_model=schemas.Sensor)
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    db_sensor = crud.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor não encontrado")
    
    deleted_sensor = crud.delete_sensor(db=db, sensor_id=sensor_id)
    return deleted_sensor