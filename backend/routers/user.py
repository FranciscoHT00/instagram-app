from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UsuarioBase, UsuarioActualizado
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import get_db
from jwt_handler import createJWT, Token, decodeJWT

router = APIRouter(
    prefix="/usuarios",
    tags=["CRUD Usuario"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(decodeJWT)]


def obtener_usuario_por_correo(correo: str, db: db_dependency):
    return db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    

@router.post("/crear")
async def crear_usuario(usuario: UsuarioBase, db: db_dependency):
    
    usuario_db = obtener_usuario_por_correo(usuario.correo, db)
    
    if usuario_db:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")
    else:    
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
        
        return {"respuesta": "Usuario creado correctamente.",
                "idUsuario": nuevo_usuario.idUsuario}
        
@router.post("/login", response_model=Token)
async def login_usuario(usuario: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    usuario_db = obtener_usuario_por_correo(usuario.username, db)
    
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Usuario no encontrado")
    if usuario.password != usuario_db.contrasenia:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Contraseña incorrecta")
    token = createJWT(usuario_db.idUsuario, usuario_db.correo)
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/listar")
async def listar_usuarios(db: db_dependency):
    result = db.query(models.Usuario).all()
    return result  

@router.get("/obtener")
async def obtener_usuario(user: user_dependency, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == user["idUsuario"]).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario

@router.patch("/actualizar")
async def actualizar_usuario(user: user_dependency, usuario_actualizado: UsuarioActualizado, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == user["idUsuario"])
    if not usuario.first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    usuario.update(usuario_actualizado.model_dump(exclude_unset=True))
    db.commit()
    return {"respuesta": "Usuario actualizado correctamente."}

@router.delete("/eliminar")
async def eliminar_usuario(user: user_dependency, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == user["idUsuario"])
    if not usuario.first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta": "Usuario eliminado correctamente."}