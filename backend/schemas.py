from pydantic import BaseModel
from datetime import datetime
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
    idUsuario: int
    nombre: str
    tipo: int
    idPublicacion: Optional[int]
    fechaInicio: datetime = datetime.now
    fechaFinal: datetime = datetime.now