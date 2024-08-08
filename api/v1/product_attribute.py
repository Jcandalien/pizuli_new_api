from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from db.models.product_attribute import AttributeCategory, ProductAttribute
from db.schemas.product_attribute import AttributeCategoryCreate, AttributeCategoryOut, ProductAttributeCreate, ProductAttributeOut
from api.deps import get_current_active_user
from pydantic import UUID4
from typing import Optional
from db.models.user import User


router = APIRouter()

@router.post("/categories", response_model=AttributeCategoryOut)
async def create_attribute_category(
    category: AttributeCategoryCreate,
    current_user: User = Depends(get_current_active_user)
):
    return await AttributeCategory.create(**category.dict())

@router.get("/categories", response_model=List[AttributeCategoryOut])
async def list_attribute_categories():
    return await AttributeCategory.all()

@router.post("/attributes", response_model=ProductAttributeOut)
async def create_product_attribute(
    attribute: ProductAttributeCreate,
    current_user: User = Depends(get_current_active_user)
):
    return await ProductAttribute.create(**attribute.dict())

@router.get("/attributes", response_model=List[ProductAttributeOut])
async def list_product_attributes(
    meat_id: Optional[UUID4] = None,
    animal_id: Optional[UUID4] = None,
    recipe_id: Optional[UUID4] = None
):
    query = ProductAttribute.all()
    if meat_id:
        query = query.filter(meat_id=meat_id)
    elif animal_id:
        query = query.filter(animal_id=animal_id)
    elif recipe_id:
        query = query.filter(recipe_id=recipe_id)
    return await query