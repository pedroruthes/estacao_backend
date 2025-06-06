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

# Vincular um sensor a um controlador
@router.post("/associate", response_model=schemas.SensorController)
def associate_sensor_controller(
    association: schemas.SensorControllerCreate,
    db: Session = Depends(get_db)
):
    db_sensor = crud.get_sensor(db, sensor_id=association.sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor não encontrado")

    db_controller = crud.get_controller(db, controller_id=association.controller_id)
    if not db_controller:
        raise HTTPException(status_code=404, detail="Controlador não encontrado")

    existing_association = crud.get_sensor_controller_association(db, association.sensor_id, association.controller_id)
    if existing_association:
        raise HTTPException(status_code=409, detail="Sensor já associado a este controlador")

    return crud.associate_sensor_with_controller(db=db, sensor_id=association.sensor_id, controller_id=association.controller_id)

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

# Desvincular um sensor de um controlador
@router.delete("/dissociate", status_code=204)
def dissociate_sensor_controller(
    association: schemas.SensorControllerCreate,
    db: Session = Depends(get_db)
):
    success = crud.dissociate_sensor_from_controller(db=db, sensor_id=association.sensor_id, controller_id=association.controller_id)
    if not success:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return


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