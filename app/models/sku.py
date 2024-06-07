from tortoise import fields, Model, Tortoise, run_async


class Sku(Model):
    sku_name = fields.CharField(max_length="50")
    height = fields.FloatField()
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
