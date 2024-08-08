from db.models.franchise import Franchise
from db.models.order import Order
from db.models.payment import Payment
from decimal import Decimal

async def process_payment(order: Order, payment_method: str):
    if payment_method == 'cash_on_delivery':
        # For cash on delivery, update the payment status to 'pending'
        payment = await Payment.create(
            order=order,
            payment_method=payment_method,
            payment_status='pending',
            amount_paid=order.total_amount,
            transaction_id=None
        )
        return payment

    # For other payment methods, process the payment
    transaction_id = f"txn_{order.id}"
    amount_paid = order.total_amount
    commission = Decimal(0.1) * order.total_amount  # Assuming a 10% commission
    franchise_payments = {}
    for item in order.items:
        franchise_id = item['franchise_id']
        if franchise_id not in franchise_payments:
            franchise_payments[franchise_id] = Decimal(0)
        franchise_payments[franchise_id] += item['price'] * item['quantity']

    payment = await Payment.create(
        order=order,
        payment_method=payment_method,
        payment_status='success',
        amount_paid=amount_paid,
        transaction_id=transaction_id
    )

    # Update the franchise payments
    for franchise_id, amount in franchise_payments.items():
        franchise = await Franchise.get(id=franchise_id)
        franchise.balance += amount - commission
        await franchise.save()

    return payment