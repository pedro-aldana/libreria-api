from pydantic import BaseModel
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    new_name: str        