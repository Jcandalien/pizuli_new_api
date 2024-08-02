
from db.models.order import Order


async def notify_logistics_partner(order: Order):
    # This is a placeholder for the actual integration with a logistics partner
    # we will make an API call to the jettts here
    return {
        "pickup_location": order.franchise.location,
        "dropoff_location": order.user.location,
        "order_details": order.items,
        "estimated_delivery_time": "2 hours"  # This will come from the jettts partner
    }