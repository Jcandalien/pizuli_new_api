from enum import Enum
from db.schemas.product_attribute import ProductAttributeOut
from pydantic import BaseModel, UUID4
from typing import Dict, List, Optional
from db.models.recipe import ProcessingStage, CookingMethod

class RecipeImageOut(BaseModel):
    id: UUID4
    image_url: str

    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    name: str
    ingredients: list
    instructions: str
    cooking_time: int
    difficulty_level: str
    processing_stage: ProcessingStage
    cooking_method: CookingMethod

class RecipeCreate(RecipeBase):
    images: Optional[List[RecipeImageOut]]
    attributes: Optional[List[ProductAttributeOut]]
    pass

class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[list] = None
    instructions: Optional[str] = None
    cooking_time: Optional[int] = None
    difficulty_level: Optional[str] = None
    processing_stage: Optional[ProcessingStage] = None
    cooking_method: Optional[CookingMethod] = None
    images: Optional[List[RecipeImageOut]]
    attributes: Optional[List[ProductAttributeOut]]

class RecipeOut(RecipeBase):
    id: UUID4
    franchise_id: UUID4
    price: float
    stock_quantity: int
    images: Optional[List[RecipeImageOut]]
    attributes: Optional[List[ProductAttributeOut]]

    class Config:
        from_attributes = True
