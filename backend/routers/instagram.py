from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas import SchemaConcurso
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import get_db
from jwt_handler import createJWT, Token, decodeJWT


router = APIRouter(
    prefix="/instagram",
    tags=["Instagram"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(decodeJWT)]

@router.get("/obtener_instagram")
async def obtener_instagram(access_token: str, request: Request):
    client = request.state.client
    req = client.build_request('GET', f"https://graph.facebook.com/v20.0/me/accounts?access_token={access_token}")
    r = await client.send(req)
    data = r.json()
    page_id = data["data"][0]["id"]
    
    req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={access_token}")
    r = await client.send(req)
    
    return r.json()

@router.get("/listar_multimedia")
async def listar_multimedia(access_token: str, instagram_id: int, request: Request):
    client = request.state.client
    req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{instagram_id}/media?access_token={access_token}")
    r = await client.send(req)
    
    return r.json()

@router.get("/obtener_multimedia")
async def obtener_multimedia(access_token: str, media_id: int, request: Request):
    client = request.state.client
    req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{media_id}?fields=id,media_type,media_url,permalink,like_count,username,timestamp&access_token={access_token}")
    r = await client.send(req)
    
    return r.json()

@router.post("/crear_concurso", tags=["Concursos"])
async def crear_concurso(concurso: SchemaConcurso, db: db_dependency):
    nuevo_concurso = models.Concurso(
        idUsuario = concurso.idUsuario,
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
    
@router.get("/listar_concursos", tags=["Concursos"])
async def listar_concursos(id_usuario: int, db: db_dependency):
    concursos = db.query(models.Concurso).filter(models.Concurso.idUsuario == id_usuario).all()
    if not concursos:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no tiene concursos creados.")
    return concursos

@router.get("/ver_participantes", tags=["Concursos"])
async def ver_participantes(id_concurso: int, access_token: str, request: Request, db: db_dependency):
    concurso = db.query(models.Concurso).filter(models.Concurso.idConcurso == id_concurso).first()
    if not concurso:
        raise HTTPException(status_code=404, detail="Concurso no encontrado.")
    else:
        if concurso.tipo == 0:
            client = request.state.client
            req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{concurso.idPublicacion}?fields=id,permalink,username,comments&access_token={access_token}")
            r = await client.send(req)
            
            data = r.json()
            lista_inicial = data["comments"]["data"]
            lista_final = set()
            for comentario in lista_inicial:
                lista_final.add(comentario["id"])
            
            return {"lista_inicial": lista_inicial, "lista_final": lista_final}
        else:
            return {"respuesta": "Aun no implementado."}