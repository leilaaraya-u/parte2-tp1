from pydantic import BaseModel, Field

class ProductoCreate(BaseModel):
    nombre: str
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")