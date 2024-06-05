from fastapi import APIRouter, Depends, HTTPException, status, Request
from schemas import SchemaConcurso
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import get_db
from jwt_handler import decodeJWT
import random


router = APIRouter(
    prefix="/concursos",
    tags=["Concursos"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(decodeJWT)]


@router.post("/crear_concurso")
async def crear_concurso(concurso: SchemaConcurso, db: db_dependency, user: user_dependency):
    
    if concurso.tipo == 0 and (concurso.idPublicacion == None or concurso.idPublicacion == 0):
        raise HTTPException(status_code=400,
                            detail="Los concursos de tipo 0 deben incluir un valor diferente a 0 en el campo idPublicacion.")
    try:
        nuevo_concurso = models.Concurso(
            idUsuario = user["idUsuario"],
            nombre=concurso.nombre,
            tipo=concurso.tipo,
            idPublicacion = concurso.idPublicacion,
            fechaInicio=concurso.fechaInicio,
            fechaFinal=concurso.fechaFinal
        )
        db.add(nuevo_concurso)
        db.commit()
        db.refresh(nuevo_concurso)
        
        return {"respuesta": "Concurso creado correctamente."}        
    except:
        return {"respuesta": "Error al crear el concurso."}   
    
    
@router.get("/listar_concursos")
async def listar_concursos(user: user_dependency, db: db_dependency):
    concursos = db.query(models.Concurso).filter(models.Concurso.idUsuario == user["idUsuario"]).all()
    if not concursos:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no tiene concursos creados.")
    return concursos

@router.get("/ver_participantes")
async def ver_participantes(id_concurso: int, request: Request, db: db_dependency, user: user_dependency):
    concurso = db.query(models.Concurso).filter(models.Concurso.idConcurso == id_concurso).first()
    if not concurso:
        raise HTTPException(status_code=404, detail="Concurso no encontrado.")
    else:
        usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == user["idUsuario"]).first()
        if concurso.tipo == 0:
            client = request.state.client
            req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{concurso.idPublicacion}?fields=id,permalink,username,comments&access_token={usuario.facebook_token}")
            r = await client.send(req)
            
            data = r.json()
            lista_inicial = data["comments"]["data"]
            lista_final = set()
            for comentario in lista_inicial:
                req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{comentario["id"]}?fields=from&access_token={usuario.facebook_token}")
                r = await client.send(req)
                data = r.json()
                lista_final.add(data["from"]["username"])
            
            return {"lista_inicial": lista_inicial, "lista_final": lista_final}        
        elif concurso.tipo == 1:
            return {"respuesta": "Aun no implementado."}
        else:
            return {"respuesta": "Aun no implementado."}
        
@router.get("/seleccionar_ganadores")
async def seleccionar_ganadores(id_concurso: int, n_ganadores: int, request: Request, db: db_dependency, user: user_dependency):
    try:
        respuesta = await ver_participantes(id_concurso, request, db, user)
        participantes = list(respuesta["lista_final"])
        
        ganadores = []
        for x in range(n_ganadores):
            if participantes:
                r = random.choice(participantes)
                ganadores.append(r)
                participantes.remove(r)                
            
        return ganadores
    except:
        raise HTTPException(status_code=404, detail="Error al obtener el listado de participantes.")
    
    
        
@router.delete("/eliminar_concurso")
async def eliminar_concurso(id_concurso: int, user: user_dependency, db: db_dependency):
    concurso = db.query(models.Concurso).filter(models.Concurso.idConcurso == id_concurso)
    if not concurso.first():
        raise HTTPException(status_code=404, detail="Concurso no encontrado.")
    
    if concurso.first().idUsuario != user["idUsuario"]:
        raise HTTPException(status_code=403, detail="Este concurso no le pertenece, no lo puede eliminar.")
    
    concurso.delete(synchronize_session=False)
    db.commit()
    return {"respuesta": "Concurso eliminado correctamente."}