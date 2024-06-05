from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    contrasenia: str
    telefono: str
    tipo: int

class UsuarioActualizado(BaseModel):
    nombre: str = None
    correo: str = None
    contrasenia: str = None
    telefono: str = None
    tipo: int = None
    
class SchemaConcurso(BaseModel):
    nombre: str
    tipo: int
    idPublicacion: Optional[int] = None
    fechaInicio: datetime = datetime.now(timezone.utc)
    fechaFinal: datetime = datetime.now(timezone.utc)
    
class SchemaPublicacion(BaseModel):
    urlImagen: str
    texto: str
    fecha: datetime = datetime.now(timezone.utc)