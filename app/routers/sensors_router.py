# Rota para receber os dados das estações meteorológicas, autenticada pela key do controlador
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/data", tags=["Dados de Sensores (SME)"])

@router.post("/", response_model=schemas.SensorMeteoSME)
def receive_meteo_data(
    data: schemas.SensorMeteoSMECreate,
    # A chave do controlador é enviada no cabeçalho "X-Controller-Key"
    x_controller_key: str = Header(..., description="Chave de Autenticação do Controlador"),
    db: Session = Depends(get_db)
):
    controller = crud.get_controller_by_key(db, key=x_controller_key)
    if not controller or not controller.enabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de controlador inválida ou controlador desabilitado."
        )
    return crud.create_sensor_meteo_sme_data(db=db, data=data, controller_id=controller.id)

@router.get("/{controller_id}", response_model=List[schemas.SensorMeteoSME])
def get_meteo_data_by_controller(
    controller_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_controller = crud.get_controller(db, controller_id=controller_id)
    if not db_controller:
        raise HTTPException(status_code=404, detail="Controlador não encontrado.")

    if start_time and end_time:
        data = crud.get_sensor_meteo_sme_data_by_controller_and_time_range(
            db, controller_id, start_time, end_time, skip=skip, limit=limit
        )
    else:
        data = crud.get_sensor_meteo_sme_data_by_controller(db, controller_id, skip=skip, limit=limit)
    return data