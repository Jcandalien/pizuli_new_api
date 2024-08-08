from tortoise import fields, models
from .base import TimestampMixin

class AnimalImage(models.Model):
    id = fields.UUIDField(pk=True)
    animal = fields.ForeignKeyField('models.Animal', related_name='animal_images')
    image_url = fields.CharField(max_length=255)


class AnimalType(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "animal_types"

class Animal(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    type = fields.ForeignKeyField('models.AnimalType', related_name='animals')
    breed = fields.CharField(max_length=50)
    age = fields.IntField()
    weight = fields.FloatField()
    health_status = fields.CharField(max_length=50)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    quantity = fields.IntField(default=1)
    owner = fields.ForeignKeyField('models.Franchise', related_name='animals')
    image = fields.CharField(max_length=255, null=True)  # Store image URL
    tags = fields.ManyToManyField('models.Tag', related_name='animals')

    class Meta:
        table = "animals"