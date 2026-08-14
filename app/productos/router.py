from fastapi import APIRouter, status
from app.database import db_productos
from app.productos.schemas import ProductoCreate

router = APIRouter()

@router.get("/")
def listar_productos():
    return db_productos

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    nuevo_prod = producto.dict()
    db_productos.append(nuevo_prod)
    return {"producto": nuevo_prod}