from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioBase, UsuarioActualizado
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import get_db

router = APIRouter(
    prefix="/usuarios",
    tags=["CRUD Usuario"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/crear")
async def crear_usuario(usuario: UsuarioBase, db: db_dependency):
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo, 
        contrasenia=usuario.contrasenia,
        telefono=usuario.telefono,
        tipo=usuario.tipo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {"respuesta": "Usuario creado correctamente."}


@router.get("/obtener/{id_usuario}")
async def obtener_usuario(id_usuario: int, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario

@router.get("/listar")
async def listar_usuarios(db: db_dependency):
    result = db.query(models.Usuario).all()
    return result

@router.patch("/actualizar/{id_usuario}")
async def actualizar_usuario(id_usuario: int, usuario_actualizado: UsuarioActualizado, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == id_usuario)
    if not usuario.first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    usuario.update(usuario_actualizado.model_dump(exclude_unset=True))
    db.commit()
    return {"respuesta": "Usuario actualizado correctamente."}

@router.delete("/eliminar")
async def eliminar_usuario(id_usuario: int, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == id_usuario)
    if not usuario.first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta": "Usuario eliminado correctamente."}