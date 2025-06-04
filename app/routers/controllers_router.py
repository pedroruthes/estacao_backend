# Rotas para gerenciar controladores
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/controllers", tags=["Controladores"])

@router.post("/", response_model=schemas.Controller)
def create_controller(
    controller: schemas.ControllerCreate,
    db: Session = Depends(get_db)
):
    db_location = crud.get_location(db, controller.location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Local não encontrado para associar o controlador")

    return crud.create_controller(db=db, controller=controller)

@router.get("/", response_model=List[schemas.Controller])
def read_controllers(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    controllers = crud.get_controllers(db, skip=skip, limit=limit)
    return controllers

@router.get("/{controller_id}", response_model=schemas.Controller)
def read_controller(
    controller_id: int,
    db: Session = Depends(get_db)
):
    db_controller = crud.get_controller(db, controller_id=controller_id)
    if db_controller is None:
        raise HTTPException(status_code=404, detail="Controlador não encontrado")
    return db_controller