# db/models/product_attribute.py
from tortoise import fields, models
from .base import TimestampMixin

class AttributeCategory(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100, unique=True)

    class Meta:
        table = "attribute_categories"

class ProductAttribute(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    category = fields.ForeignKeyField('models.AttributeCategory', related_name='attributes')
    name = fields.CharField(max_length=100)
    value = fields.CharField(max_length=100)
    meat = fields.ForeignKeyField('models.Meat', related_name='attributes', null=True)
    animal = fields.ForeignKeyField('models.Animal', related_name='attributes', null=True)
    recipe = fields.ForeignKeyField('models.Recipe', related_name='attributes', null=True)

    class Meta:
        table = "product_attributes"


"""
below are the proposed categories for products


1. Origin
    - Local breed or imported
    - Wild game or farm-raised
2. Feed
    - Grass-fed or grain-fed
    - Organic or non-organic
3. Treatment
    - Hormone-free or hormone-injected
    - Antibiotic-free or antibiotic-treated
4. Religious Certification
    - Halal or non-halal
5. Breed/Quality
    - Wagyu or non-Wagyu (for beef)
    - Marbling score (for beef)
    - Certifications (UNBS, ISO, etc.)
6. Slaughter Method
    - Method of slaughter (humane, traditional)
7. Product Quality
    - Cut and trim quality
    - Packaging and storage methods
8. Pricing
    - Price per pound or kilogram
9. Additional
    - Fresh or frozen"""