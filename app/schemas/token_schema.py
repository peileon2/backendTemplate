from tortoise import fields
from tortoise.models import Model


class Message(Model):
    message = fields.CharField(max_length=255)


class Token(Model):
    access_token = fields.CharField(max_length=255)
    token_type = fields.CharField(max_length=255, default="bearer")


class TokenPayload(Model):
    sub = fields.IntField(null=True)


class NewPassword(Model):
    token = fields.CharField(max_length=255)
    new_password = fields.CharField(max_length=255)


# Properties to return via API, id is always required
class UserPublic(Model):
    id = fields.IntField(null=True)


class UsersPublic(Model):
    # 使用 UserPublic 类作为字段类型
    data = fields.JSONField()
    count = fields.IntField()
