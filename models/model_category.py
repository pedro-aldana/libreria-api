from tortoise import Model,fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .model_book import Book

class Category(Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True, null=False)

    created_at = fields.DatetimeField(auto_now_add=True)

    books = fields.ReverseRelation["Book"]
    
    def __repr__(self):
        return f"<Category {self.name}>"