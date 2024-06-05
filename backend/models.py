from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Boolean
from database import Base, engine

class Usuario(Base):
    __tablename__  = 'Usuario'
    
    idUsuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True, index=True)
    contrasenia = Column(String)    
    telefono = Column(String)
    tipo = Column(Integer)
    idInstagram = Column(BigInteger)
    facebook_token = Column(String)

class Concurso(Base):
    __tablename__ = 'Concurso'
    
    idConcurso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idUsuario = Column(Integer, ForeignKey("Usuario.idUsuario"))
    nombre = Column(String)
    tipo = Column(Integer)
    idPublicacion = Column(BigInteger)
    fechaInicio = Column(DateTime)
    fechaFinal = Column(DateTime)
    
class Publicacion(Base):
    __tablename__ = 'Publicacion'
    
    idPublicacion = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idUsuario = Column(Integer, ForeignKey("Usuario.idUsuario"))
    urlImagen = Column(String)
    texto = Column(String)
    fecha = Column(DateTime)
    publicada = Column(Boolean)
    urlPublicacion = Column(String)
    
    
Base.metadata.create_all(bind=engine)