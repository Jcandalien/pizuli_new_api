from tortoise import fields, models
from .order import Order
from enum import IntEnum

class DeliveryStatus(IntEnum):
    PENDING = 1
    PICKED_UP = 2
    IN_TRANSIT = 3
    DELIVERED = 4
    FAILED = 5

class Delivery(models.Model):
    id = fields.UUIDField(pk=True)
    order = fields.ForeignKeyField('models.Order', related_name='delivery')
    status = fields.IntEnumField(DeliveryStatus, default=DeliveryStatus.PENDING)
    assigned_to = fields.ForeignKeyField('models.User', related_name='deliveries')
    pickup_locations = fields.JSONField()
    dropoff_location = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "deliveries"