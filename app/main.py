from fastapi import FastAPI, Depends
from app.usuarios.router import router as usuarios_router
from app.productos.router import router as productos_router
from app.productos.dependencies import verify_api_token

app = FastAPI(title="Sistema de Productos y Usuarios - TP2")

# Router de usuarios (sin proteccion global)
app.include_router(usuarios_router, prefix="/users")

# Router de productos (protegido globalmente con la dependencia)
app.include_router(
    productos_router, 
    prefix="/products", 
    dependencies=[Depends(verify_api_token)]
)