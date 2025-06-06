# O ponto de entrada da aplicação
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import data_router, locations_router, controllers_router, sensors_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Estações Meteorológicas (MVP)",
    description="Backend para cadastrar locais, controladores e receber dados de estações meteorológicas.",
    version="0.1.0",
)

app.include_router(locations_router.router)
app.include_router(controllers_router.router)
app.include_router(data_router.router)
app.include_router(sensors_router.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Estações Meteorológicas!"}