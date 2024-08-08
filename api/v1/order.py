from db.models.recipe import Recipe
from db.schemas.recipe import RecipeCreate, RecipeOut
from fastapi import APIRouter, Depends, HTTPException, status,Query
from pydantic import UUID4
from db.models.franchise import Franchise
from db.models.order import Order, OrderStatus
from db.models.user import User
from db.schemas.order import OrderCreate, OrderUpdate, OrderOut
from api.deps import get_current_active_user
from services.franchise import get_nearest_open_franchises, is_franchise_open
from services.order_processing import process_order, update_order_status
from services.logistics import notify_logistics_partner
from typing import List

from services.payment import process_payment
from services.product import get_product_by_id
from services.recipes import notify_franchises, wait_for_recipe_acceptance
from utils.distance import haversine_distance

router = APIRouter()

@router.post("/", response_model=OrderOut)
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_active_user)
):
    # Find the nearest franchise
    franchises = await Franchise.all()
    nearest_franchise = min(
        franchises,
        key=lambda f: haversine_distance(
            current_user.latitude, current_user.longitude,
            f.latitude, f.longitude
        )
    )

    # Create the order with the nearest franchise
    order = await Order.create(**order_in.dict(), user=current_user, franchise=nearest_franchise)
    # Process payment
    # payment_info = await process_payment(order)
    # if payment_info["status"] != "success":
    #     await order.delete()
    #     raise HTTPException(status_code=400, detail="Payment failed")

    processed_order = await process_order(order.id)
     # Update order with payment information
    # processed_order.payment_info = payment_info
    # await processed_order.save()

    return processed_order


@router.post("/", response_model=OrderOut)
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    lat: float = Query(...),
    lon: float = Query(...)
):
    # Group items by franchise
    franchise_orders = {}
    for item in order_in.items:
        product, product_type = await get_product_by_id(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

        franchise_id = product.franchise_id if product_type in ['meat', 'recipe'] else product.owner_id
        if franchise_id not in franchise_orders:
            franchise_orders[franchise_id] = []
        franchise_orders[franchise_id].append((item, product, product_type))

    # Create an order for each franchise
    orders = []
    for franchise_id, items in franchise_orders.items():
        franchise = await Franchise.get(id=franchise_id)
        if not await is_franchise_open(franchise):
            raise HTTPException(status_code=400, detail=f"Franchise {franchise.name} is closed")

        order_items = [
            {
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "price": product.price,
                "product_type": product_type
            } for item, product, product_type in items
        ]

        order = await Order.create(
            user=current_user,
            franchise=franchise,
            items=order_items,
            total_amount=sum(item["price"] * item["quantity"] for item in order_items),
            status=OrderStatus.PENDING
        )
        orders.append(order)

    # Process orders
    processed_orders = [await process_order(order.id) for order in orders]

    # Notify logistics partner
    try:
        logistics_response = await notify_logistics_partner(processed_orders)
    except Exception as e:
        # If logistics partner fails, use fallback mechanism
        logistics_response = await notify_fallback_delivery(processed_orders)

    # Update orders with logistics information
    for order in processed_orders:
        order.logistics_info = logistics_response
        await order.save()

    return processed_orders



@router.get("/", response_model=List[OrderOut])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    orders = await Order.filter(user=current_user).offset(skip).limit(limit)
    return orders


@router.get("/{order_id}", response_model=OrderOut)
async def read_order(
    order_id: UUID4,
    current_user: User = Depends(get_current_active_user)
):
    order = await Order.get_or_none(id=order_id, user=current_user)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}/status", response_model=OrderOut)
async def update_order(
    order_id: UUID4,
    new_status: OrderStatus,
    current_user: User = Depends(get_current_active_user)
):
    order = await Order.get_or_none(id=order_id, user=current_user)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await update_order_status(order.id, new_status)
    return updated_order


@router.post("/order-on-demand", response_model=RecipeOut)
async def create_on_demand_recipe(
    recipe: RecipeCreate,
    current_user: User = Depends(get_current_active_user),
    lat: float = Query(...),
    lon: float = Query(...)
):
    # Get nearest open franchises
    nearest_franchises = await get_nearest_open_franchises(lat, lon, limit=5)

    if not nearest_franchises:
        raise HTTPException(status_code=404, detail="No open franchises found nearby")

    # Create a pending recipe
    pending_recipe = await Recipe.create(**recipe.dict(), status="PENDING")

    # Notify franchises about the new recipe request
    await notify_franchises(nearest_franchises, pending_recipe)

    # Wait for a franchise to accept (you might want to implement this as a background task)
    accepted_recipe = await wait_for_recipe_acceptance(pending_recipe.id, timeout=300)  # 5 minutes timeout

    if not accepted_recipe:
        await pending_recipe.delete()
        raise HTTPException(status_code=408, detail="No franchise accepted the recipe request")

    return accepted_recipe