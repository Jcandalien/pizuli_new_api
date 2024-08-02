from tortoise import fields, models
from .base import TimestampMixin

class Tag(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "tags"