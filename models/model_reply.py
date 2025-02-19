from tortoise import Model, fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model_comment import Comment
    from model_user import User


class Reply(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    user = fields.ForeignKeyField('models.User', related_name='replies')
    comment = fields.ForeignKeyField('models.Comment', related_name='replies')

    created_at = fields.DatetimeField(auto_now_add=True)