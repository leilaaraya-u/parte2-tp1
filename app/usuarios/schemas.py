from pydantic import BaseModel, field_validator

class UsuarioCreate(BaseModel):
    username: str
    edad: int

    @field_validator("username")
    @classmethod
    def validar_username(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("El username debe tener al menos 5 caracteres")
        return v

    @field_validator("edad")
    @classmethod
    def validar_edad(cls, v: int) -> int:
        if v < 18:
            raise ValueError("La edad debe ser mayor o igual a 18 años")
        return v