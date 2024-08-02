from tortoise import fields, models
from .base import TimestampMixin
from enum import IntEnum

class OrderStatus(IntEnum):
    PENDING = 1
    PROCESSING = 2
    SHIPPED = 3
    DELIVERED = 4
    CANCELLED = 5

class Order(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='orders')
    franchise = fields.ForeignKeyField('models.Franchise', related_name='orders')
    items = fields.JSONField()  # Store order items as JSON
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    status = fields.IntEnumField(OrderStatus, default=OrderStatus.PENDING)

    class Meta:
        table = "orders"