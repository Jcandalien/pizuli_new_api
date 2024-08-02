from tortoise import fields, models
from .base import TimestampMixin

class User(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    fullname = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)

    class Meta:
        table = "users"