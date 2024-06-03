from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from database import Base

class Usuario(Base):
    __tablename__  = 'Usuario'
    
    idUsuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True, index=True)
    contrasenia = Column(String)    
    telefono = Column(String)
    tipo = Column(Integer)

class Concurso(Base):
    __tablename__ = 'Concurso'
    
    idConcurso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idUsuario = Column(Integer, ForeignKey("Usuario.idUsuario"))
    nombre = Column(String)
    tipo = Column(Integer)
    idPublicacion = Column(BigInteger)
    fechaInicio = Column(DateTime)
    fechaFinal = Column(DateTime)