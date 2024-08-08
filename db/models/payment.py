from tortoise import fields, models
from .order import Order

class Payment(models.Model):
    id = fields.UUIDField(pk=True)
    order = fields.OneToOneField('models.Order', related_name='payment')
    payment_method = fields.CharField(max_length=50)
    payment_status = fields.CharField(max_length=50)
    amount_paid = fields.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "payments"