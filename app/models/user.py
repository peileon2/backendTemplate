from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)  # 自动递增的主键字段
    email = fields.CharField(unique=True, index=True, max_length=255)
    hashed_password = fields.CharField(unique=True, index=True, max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    full_name = fields.CharField(max_length=255, null=True)
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
