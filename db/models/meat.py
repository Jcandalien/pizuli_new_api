from tortoise import fields, models
from .base import TimestampMixin

class MeatImage(models.Model):
    id = fields.UUIDField(pk=True)
    meat = fields.ForeignKeyField('models.Meat', related_name='meat_images')
    image_url = fields.CharField(max_length=255)



class MeatType(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "meat_types"

class Meat(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    type = fields.ForeignKeyField('models.MeatType', related_name='meats')
    cut = fields.CharField(max_length=50)
    grade = fields.CharField(max_length=20)
    weight = fields.FloatField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    is_frozen = fields.BooleanField(default=False)
    is_fresh = fields.BooleanField(default=True)
    franchise = fields.ForeignKeyField('models.Franchise', related_name='meats')
    stock_quantity = fields.IntField(default=0)
    tags = fields.ManyToManyField('models.Tag', related_name='meats')
    is_chilled = fields.BooleanField(default=False)

    class Meta:
        table = "meats"