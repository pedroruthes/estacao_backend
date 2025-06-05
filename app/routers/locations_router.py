# app/routers/locations_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/locations", tags=["Locais"])

# Cria um novo local
@router.post("/", response_model=schemas.Location)
def create_location(
    location: schemas.LocationCreate,
    db: Session = Depends(get_db)
):
    return crud.create_location(db=db, location=location)

# Retorna todos os locais cadastrados, com paginação opcional
@router.get("/", response_model=List[schemas.Location])
def read_locations(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations

# Retorno os dados de um local pelo ID
@router.get("/{location_id}", response_model=schemas.Location)
def read_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return db_location

# Atualiza um local existente pelo ID
@router.patch("/{location_id}", response_model=schemas.Location)
def update_location(
    location_id: int,
    location: schemas.LocationUpdate,
    db: Session = Depends(get_db)
):
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Local não encontrado para atualização")
    
    update_data = location.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    
    updated_location = crud.update_location(db=db, db_location=db_location, location_update=location)
    return updated_location