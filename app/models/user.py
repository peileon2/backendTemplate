from tortoise import fields, models


class User(models.Model):
    email = fields.CharField(unique=True, index=True, max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    full_name = fields.CharField(max_length=255, null=True)
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
