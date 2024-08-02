from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime
from enum import Enum

from db.models.order import OrderStatus


class OrderItem(BaseModel):
    product_id: UUID4
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_price: float
    address: str

class OrderUpdate(BaseModel):
    status: OrderStatus

class OrderOut(BaseModel):
    id: UUID4
    user_id: UUID4
    franchise_id: UUID4
    items: List[OrderItem]
    total_price: float
    address: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True