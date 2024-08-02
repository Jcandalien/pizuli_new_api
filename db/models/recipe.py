from enum import Enum
from tortoise import fields, models
from .base import TimestampMixin

class ProcessingStage(str, Enum):
    RAW = "raw"
    COOKED = "cooked"

class CookingMethod(str, Enum):
    ROASTED = "roasted"
    FRIED = "fried"
    BOILED = "boiled"
    GRILLED = "grilled"
    STEAMED = "steamed"
    BAKED = "baked"

class RecipeImage(models.Model):
    id = fields.UUIDField(pk=True)
    recipe = fields.ForeignKeyField('models.Recipe', related_name='images')
    image_url = fields.CharField(max_length=255)

class Recipe(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100)
    ingredients = fields.JSONField()
    instructions = fields.TextField()
    cooking_time = fields.IntField()  # in minutes
    difficulty_level = fields.CharField(max_length=20)
    is_raw_material = fields.BooleanField(default=False)
    franchise = fields.ForeignKeyField('models.Franchise', related_name='recipes')
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = fields.IntField(default=0)
    tags = fields.ManyToManyField('models.Tag', related_name='recipes')
    rating = fields.FloatField(default=0.0)
    review_count = fields.IntField(default=0)
    processing_stage = fields.CharEnumField(ProcessingStage)
    cooking_method = fields.CharEnumField(CookingMethod)

    class Meta:
        table = "recipes"