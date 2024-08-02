from tortoise import fields, models
from .base import TimestampMixin

class Review(models.Model, TimestampMixin):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='reviews')
    franchise = fields.ForeignKeyField('models.Franchise', related_name='reviews', null=True)
    recipe = fields.ForeignKeyField('models.Recipe', related_name='reviews', null=True)
    rating = fields.FloatField()
    comment = fields.TextField()
    is_flagged = fields.BooleanField(default=False)

    class Meta:
        table = "reviews"