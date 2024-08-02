from tortoise import fields, models
from enum import IntEnum
from .base import TimestampMixin

class FranchiseType(IntEnum):
    FARMER = 1
    BUTCHER = 2
    MEAT_STORE = 3
    RESTAURANT = 4

class Franchise(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100)
    type = fields.IntEnumField(FranchiseType)  # This uses the IntEnumField provided by Tortoise
    owner = fields.ForeignKeyField('models.User', related_name='franchises')
    location = fields.CharField(max_length=255)
    description = fields.TextField()
    rating = fields.FloatField(default=0.0)
    review_count = fields.IntField(default=0)
    is_approved = fields.BooleanField(default=False)
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)

    class Meta:
        table = "franchises"

