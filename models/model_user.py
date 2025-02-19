from tortoise import Model,fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model_book import Book
    from model_comment import Comment


class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True)

    users: fields.ReverseRelation["User"]

    def __repr__(self):
        return f"<Role {self.name}>"


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True, null=False)
    username = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255, null=False)
    banner_img = fields.CharField(max_length=300,null=True)
    profile_img = fields.CharField(max_length=300,null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    role: fields.ForeignKeyRelation["Role"] = fields.ForeignKeyField(
        "models.Role", related_name="users", null=True
    )

    books: fields.ReverseRelation["Book"]
    comments: fields.ReverseRelation["Comment"]


    def __repr__(self):
        return f"<User {self.username} email={self.email}>"
