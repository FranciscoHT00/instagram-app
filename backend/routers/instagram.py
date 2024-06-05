from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import get_db
from jwt_handler import decodeJWT


router = APIRouter(
    prefix="/instagram",
    tags=["Instagram"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(decodeJWT)]

@router.patch("/enlazar_instagram")
async def enlazar_instagram(access_token: str, request: Request, user: user_dependency, db: db_dependency):
    
    client = request.state.client
    try:
        req = client.build_request('GET', f"https://graph.facebook.com/v20.0/me/accounts?access_token={access_token}")
        r = await client.send(req)
        data = r.json()
        page_id = data["data"][0]["id"]
        
        req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={access_token}")
        r = await client.send(req)
        data = r.json()
        idInstagram = int(data["instagram_business_account"]["id"])
        
        usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == user["idUsuario"])
        if not usuario.first():
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
        try:
            usuario.update({"idInstagram": idInstagram, "facebook_token": access_token})
            db.commit()
        
            return {"respuesta": "Datos de instagram guardados correctamente",
                    "idInstagram": idInstagram,
                    "facebook_token": access_token}
        except:
            return {"respuesta": "Error base de datos"}
        
    except:
        return {"respuesta": "Error al guardar los datos de instagram",
                "data": data}    


@router.get("/listar_multimedia")
async def listar_multimedia(user: user_dependency, db: db_dependency, request: Request):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == user["idUsuario"]).first()
    instagram_id = usuario.idInstagram
    access_token = usuario.facebook_token
    
    if instagram_id is None or access_token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Para acceder a esta funcionalidad debes enlazar tu cuenta de Instagram")
    else:
        client = request.state.client
        req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{instagram_id}/media?access_token={access_token}")
        r = await client.send(req)
    
        return r.json()
    

@router.get("/obtener_multimedia")
async def obtener_multimedia(user: user_dependency, db: db_dependency, media_id: int, request: Request):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == user["idUsuario"]).first()
    instagram_id = usuario.idInstagram
    access_token = usuario.facebook_token
    
    if instagram_id is None or access_token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Para acceder a esta funcionalidad debes enlazar tu cuenta de Instagram")
    else:
        client = request.state.client
        req = client.build_request('GET', f"https://graph.facebook.com/v20.0/{media_id}?fields=id,media_type,media_url,permalink,like_count,username,timestamp,caption&access_token={access_token}")
        r = await client.send(req)
        
        return r.json()
