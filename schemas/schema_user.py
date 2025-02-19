from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class RoleOut(BaseModel):
    """Esquema para la respuesta de un rol."""
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    """Esquema para la creación de un usuario."""
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    """Esquema para la respuesta al obtener un usuario."""
    id: int
    email: EmailStr
    username: str
    profile_img: Optional[str] = None  # Campo opcional
    banner_img: Optional[str] = None  # Campo opcional
    created_at: datetime
    role: RoleOut

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    """Esquema para la actualización parcial de un usuario."""
    new_username: Optional[str] = None
    new_password: Optional[str] = None
    new_role_id: Optional[int] = None
    new_profile_img: Optional[str] = None
    new_banner_img: Optional[str] = None

class UserLogin(BaseModel):
    """Esquema para la autenticación del usuario."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Esquema para la respuesta al iniciar sesión."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Esquema para extraer información del token."""
    email: Optional[str] = None
    role: Optional[str] = None
