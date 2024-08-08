from pydantic import BaseModel, UUID4
from typing import List, Optional

class AttributeCategoryBase(BaseModel):
    name: str

class AttributeCategoryCreate(AttributeCategoryBase):
    pass

class AttributeCategoryOut(AttributeCategoryBase):
    id: UUID4

    class Config:
        from_attributes = True

class ProductAttributeBase(BaseModel):
    category_id: UUID4
    name: str
    value: str

class ProductAttributeCreate(ProductAttributeBase):
    meat_id: Optional[UUID4] = None
    animal_id: Optional[UUID4] = None
    recipe_id: Optional[UUID4] = None

class ProductAttributeOut(ProductAttributeBase):
    id: UUID4

    class Config:
        from_attributes = True

# Update existing schemas (meat.py, animal.py, recipe.py) to include new fields and relationships
# For example, in db/schemas/meat.py:
