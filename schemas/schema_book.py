from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserOut(BaseModel):
    id: int
    username: str
    email: str

class CategoryOut(BaseModel):
    id: int
    name: str

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    rating: int
    archive: str 

class BookCreate(BookBase):
    category_id: int  # Se mantiene el ID para la creación

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None

class BookOut(BookBase):
    id: int
    created_at: datetime
    user: Optional[UserOut]  # Hacer opcional si puede ser None
    category: Optional[CategoryOut]  # Hacer opcional si puede ser None

    class Config:
        from_attributes = True

