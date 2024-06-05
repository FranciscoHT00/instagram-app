from fastapi import APIRouter, Depends, HTTPException, status, Request
from schemas import SchemaPublicacion
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import get_db
from jwt_handler import decodeJWT
from datetime import datetime, timezone, timedelta


router = APIRouter(
    prefix="/publicaciones",
    tags=["Publicaciones"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(decodeJWT)]


@router.post("/programar_publicacion")
async def programar_publicacion(publicacion: SchemaPublicacion, db: db_dependency, user: user_dependency):
        
    try:
        
        nueva_publicacion = models.Publicacion(
            idUsuario = user["idUsuario"],
            urlImagen = publicacion.urlImagen,
            texto = publicacion.texto,
            fecha= publicacion.fecha,
            publicada= False,
            urlPublicacion = None
        )
        db.add(nueva_publicacion)
        db.commit()
        db.refresh(nueva_publicacion)
        
        return {"respuesta": "Publicacion programada correctamente.", "id": nueva_publicacion.idPublicacion}        
    except:
        return {"respuesta": "Error al programar la publicacion."}

@router.get("/listar_publicaciones_programadas")
async def listar_publicaciones_programadas(user: user_dependency, db: db_dependency):
    publicaciones = db.query(models.Publicacion).filter(models.Publicacion.idUsuario == user["idUsuario"]).all()
    if not publicaciones:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no tiene publicaciones programadas.")
    return publicaciones

@router.delete("/cancelar_publicacion_programada")
async def cancelar_publicacion_programada(id_publicacion: int, user: user_dependency, db: db_dependency):
    publicacion = db.query(models.Publicacion).filter(models.Publicacion.idPublicacion == id_publicacion)
    if not publicacion.first():
        raise HTTPException(status_code=404, detail="Publicacion no encontrada.")
    
    if publicacion.first().idUsuario != user["idUsuario"]:
        raise HTTPException(status_code=403, detail="Esta publicacion no le pertenece, no la puede eliminar.")
    
    publicacion.delete(synchronize_session=False)
    db.commit()
    return {"respuesta": "Publicacion eliminado correctamente."}