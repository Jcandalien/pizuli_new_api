from core.security import get_password_hash
from db.models.delivery import Delivery, DeliveryStatus
from db.models.order import Order, OrderStatus
from db.models.user import User

async def get_fallback_delivery_user():
    fallback_user = await User.get_or_none(is_fallback_delivery_user=True)
    if not fallback_user:
        fallback_user = await User.create_fallback_delivery_user(
            username="jcmbisa",
            fullname="jean Claude",
            email="jcmbisa@gmail.com",
            hashed_password=get_password_hash("testpass123")
        )
    return fallback_user

async def notify_fallback_delivery(orders):
    fallback_user = await get_fallback_delivery_user()
    deliveries = []
    for order in orders:
        delivery = await Delivery.create(
            order=order,
            status=DeliveryStatus.PENDING,
            assigned_to=fallback_user
        )
        order.status = OrderStatus.PROCESSING
        await order.save()
        deliveries.append(delivery)
    return [delivery.id for delivery in deliveries]