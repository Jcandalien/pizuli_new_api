from fastapi import APIRouter, Query
from db.models.animal import Animal
from db.models.meat import Meat
from db.models.recipe import CookingMethod, ProcessingStage, Recipe
from db.schemas.animal import AnimalOut
from db.schemas.meat import MeatOut
from db.schemas.recipe import RecipeOut
from typing import List, Optional, Union

router = APIRouter()

ProductOut = Union[AnimalOut, MeatOut, RecipeOut]

ProductOut = Union[AnimalOut, MeatOut, RecipeOut]

@router.get("/", response_model=List[ProductOut])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    product_type: Optional[str] = Query(None, enum=["animal", "meat", "recipe"]),
    search: Optional[str] = Query(None),
    processing_stage: Optional[ProcessingStage] = Query(None),
    cooking_method: Optional[CookingMethod] = Query(None)
):
    queries = []

    if product_type is None or product_type == "animal":
        animal_query = Animal.all()
        if search:
            animal_query = animal_query.filter(breed__icontains=search)
        queries.append(animal_query)

    if product_type is None or product_type == "meat":
        meat_query = Meat.all()
        if search:
            meat_query = meat_query.filter(cut__icontains=search)
        queries.append(meat_query)

    if product_type is None or product_type == "recipe":
        recipe_query = Recipe.all()
        if search:
            recipe_query = recipe_query.filter(name__icontains=search)
        if processing_stage:
            recipe_query = recipe_query.filter(processing_stage=processing_stage)
        if cooking_method:
            recipe_query = recipe_query.filter(cooking_method=cooking_method)
        queries.append(recipe_query)

    # Combine results
    all_products = []
    for query in queries:
        products = await query.offset(skip).limit(limit)
        all_products.extend(products)

    # Sort by a common attribute or use a custom sorting function
    def sort_key(product):
        if isinstance(product, Animal):
            return product.breed
        elif isinstance(product, Meat):
            return product.cut
        elif isinstance(product, Recipe):
            return product.name
        return ""

    all_products.sort(key=sort_key)

    return all_products[:limit]