from tortoise import Model, fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.model_user import User
    from models.model_category import Category
    from models.model_comment import Comment

class Book(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, null=False)
    author = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    cover_image = fields.CharField(max_length=255, null=True)
    rating = fields.IntField()
    archive = fields.CharField(max_length=300,null=False)

    created_at = fields.DatetimeField(auto_now_add=True)

    user = fields.ForeignKeyField('models.User', related_name='books')
    category = fields.ForeignKeyField('models.Category', related_name='books')

    comments: fields.ReverseRelation["Comment"]
    


    def __repr__(self):
        return f"<Book {self.title} author={self.author}>"