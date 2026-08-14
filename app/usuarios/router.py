from fastapi import APIRouter, HTTPException, status, Path
from app.database import db_usuarios
from app.usuarios.schemas import UsuarioCreate

router = APIRouter()

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate):
    for u in db_usuarios:
        if u.get("username") == usuario.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe en la base de datos"
            )
    
    nuevo_id = len(db_usuarios) + 1
    nuevo_usuario = usuario.dict()
    nuevo_usuario["id"] = nuevo_id
    
    if not nuevo_usuario.get("categoria"):
        nuevo_usuario["categoria"] = "general"
        
    db_usuarios.append(nuevo_usuario)
    return {"usuario": nuevo_usuario}  # <-- Clave "usuario" para el test

@router.get("/{user_id}")
def obtener_usuario(user_id: int = Path(..., gt=0)):
    for u in db_usuarios:
        if u.get("id") == user_id:
            return u
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )