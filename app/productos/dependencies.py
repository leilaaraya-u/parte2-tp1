from fastapi import Header, HTTPException, status
from typing import Optional
from typing_extensions import Annotated

def verify_api_token(x_token: Annotated[Optional[str], Header()] = None):
    if x_token != "secret123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o ausente"
        )