from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from decouple import config
from typing import Annotated
from starlette import status
from pydantic import BaseModel
import time
import jwt


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

class Token(BaseModel):
    access_token: str
    token_type: str
    

def createJWT(idUsuario: int, correo: str):
    payload = {
        "idUsuario": idUsuario,
        "correo": correo,
        "expiry": time.time() + 600
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

async def decodeJWT(token: Annotated[str, Depends(oauth2_scheme)]):
    try:        
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        idUsuario = payload.get("idUsuario")
        correo = payload.get("correo")
        if idUsuario is None or correo is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="No se pudo validar al usuario")
        return {"idUsuario": idUsuario, "correo": correo}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="No se pudo validar al usuario")

    
    