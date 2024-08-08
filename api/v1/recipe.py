from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import UUID4
from api.deps import get_approved_franchise
from db.models.franchise import Franchise
from db.models.recipe import Recipe, ProcessingStage, CookingMethod
from db.schemas.recipe import RecipeCreate, RecipeOut, RecipeUpdate
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[RecipeOut])
async def read_recipes(
    skip: int = 0,
    limit: int = 100,
    processing_stage: Optional[ProcessingStage] = Query(None),
    cooking_method: Optional[CookingMethod] = Query(None),
    min_cooking_time: Optional[int] = Query(None),
    max_cooking_time: Optional[int] = Query(None),
    difficulty_level: Optional[str] = Query(None),
    attribute_name: Optional[str] = Query(None),
    attribute_value: Optional[str] = Query(None),
    is_franchise_open: Optional[bool] = Query(None)
):
    query = Recipe.all().prefetch_related("franchise")
    if is_franchise_open is not None:
        query = query.filter(franchise__is_open=is_franchise_open)
    if processing_stage:
        query = query.filter(processing_stage=processing_stage)
    if cooking_method:
        query = query.filter(cooking_method=cooking_method)
    if min_cooking_time is not None:
        query = query.filter(cooking_time__gte=min_cooking_time)
    if max_cooking_time is not None:
        query = query.filter(cooking_time__lte=max_cooking_time)
    if difficulty_level:
        query = query.filter(difficulty_level=difficulty_level)
    if attribute_name and attribute_value:
        query = query.filter(attributes__name=attribute_name, attributes__value=attribute_value)

    recipes = await query.offset(skip).limit(limit)
    return recipes


@router.post("/", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_in: RecipeCreate,
    franchise: Franchise = Depends(get_approved_franchise)
):
    recipe = await Recipe.create(**recipe_in.dict(), franchise=franchise)
    return recipe


@router.put("/{recipe_id}", response_model=RecipeOut)
async def update_recipe(
    recipe_id: UUID4,
    recipe_in: RecipeUpdate,
    franchise: Franchise = Depends(get_approved_franchise)
):
    recipe = await Recipe.get_or_none(id=recipe_id, franchise=franchise)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_data = recipe_in.dict(exclude_unset=True)
    for field, value in recipe_data.items():
        setattr(recipe, field, value)
    await recipe.save()
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: UUID4,
    franchise: Franchise = Depends(get_approved_franchise)
):
    recipe = await Recipe.get_or_none(id=recipe_id, franchise=franchise)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    await recipe.delete()
    return {"ok": True}


