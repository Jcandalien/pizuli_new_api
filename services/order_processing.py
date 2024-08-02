from db.models.order import Order, OrderStatus
from db.models.meat import Meat
from db.models.recipe import Recipe
from fastapi import HTTPException
from tortoise.transactions import atomic

@atomic()
async def process_order(order_id: int):
    """
    Process an order: check stock, update quantities, and change order status.
    """
    order = await Order.get_or_none(id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Order is not in pending status")

    for item in order.items:
        if item['type'] == 'meat':
            meat = await Meat.get_or_none(id=item['id'])
            if not meat or meat.stock_quantity < item['quantity']:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for meat item {item['id']}")
            meat.stock_quantity -= item['quantity']
            await meat.save()
        elif item['type'] == 'recipe':
            recipe = await Recipe.get_or_none(id=item['id'])
            if not recipe or recipe.stock_quantity < item['quantity']:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for recipe item {item['id']}")
            recipe.stock_quantity -= item['quantity']
            await recipe.save()

    order.status = OrderStatus.PROCESSING
    await order.save()
    return order

async def update_order_status(order_id: int, new_status: OrderStatus):
    """
    Update the status of an order.
    """
    order = await Order.get_or_none(id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = new_status
    await order.save()
    return order