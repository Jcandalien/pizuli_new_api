
from db.models.order import Order


async def process_payment(order: Order):
    # This is a placeholder for the integration with a payment processor,  we will make an API call to the payment processor here
    payment_info = {
        "amount": order.total_amount,
        "currency": "UGX",
        "payment_method": "credit_card",
        "status": "success",
        "transaction_id": f"txn_{order.id}"
    }
    return payment_info