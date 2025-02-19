from tortoise import Model, fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.model_reply import Reply

class Comment(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    user = fields.ForeignKeyField('models.User', related_name='comments')
    book = fields.ForeignKeyField('models.Book', related_name='comments')

    replies: fields.ReverseRelation['Reply']

    created_at = fields.DatetimeField(auto_now_add=True)

    