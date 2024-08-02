from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import UUID4
from db.models.animal import Animal, AnimalType
from db.models.franchise import Franchise
from db.models.user import User
from db.schemas.animal import AnimalCreate, AnimalTypeCreate, AnimalTypeOut, AnimalUpdate, AnimalOut
from api.deps import get_current_active_superuser, get_current_active_user, get_approved_franchise
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=AnimalOut)
async def create_animal(
    animal_in: AnimalCreate,
    # franchise: Franchise = Depends(get_approved_franchise)
):
    animal_type = await AnimalType.get_or_none(id=animal_in.type_id)
    if not animal_type:
        raise HTTPException(status_code=404, detail="Animal type not found")

    animal = await Animal.create(**animal_in.dict(), owner=None, type=animal_type)
    return animal

@router.get("/", response_model=List[AnimalOut])
async def read_animals(
    skip: int = 0,
    limit: int = 100,
    animal_type_id: Optional[UUID4] = Query(None),
    breed: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None),
    max_age: Optional[int] = Query(None),
    min_weight: Optional[float] = Query(None),
    max_weight: Optional[float] = Query(None)
):
    query = Animal.all()
    if animal_type_id:
        query = query.filter(type_id=animal_type_id)
    if breed:
        query = query.filter(breed=breed)
    if min_age is not None:
        query = query.filter(age__gte=min_age)
    if max_age is not None:
        query = query.filter(age__lte=max_age)
    if min_weight is not None:
        query = query.filter(weight__gte=min_weight)
    if max_weight is not None:
        query = query.filter(weight__lte=max_weight)

    animals = await query.offset(skip).limit(limit)
    return animals


@router.get("/{animal_id}", response_model=AnimalOut)
async def read_animal(animal_id: UUID4):
    animal = await Animal.get_or_none(id=animal_id)
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.put("/{animal_id}", response_model=AnimalOut)
async def update_animal(
    animal_id: UUID4,
    animal_in: AnimalUpdate,
    franchise: Franchise = Depends(get_approved_franchise)
):
    animal = await Animal.get_or_none(id=animal_id, owner=franchise)
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    animal_data = animal_in.dict(exclude_unset=True)
    for field, value in animal_data.items():
        setattr(animal, field, value)
    await animal.save()
    return animal


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(
    animal_id: UUID4,
    franchise: Franchise = Depends(get_approved_franchise)
):
    animal = await Animal.get_or_none(id=animal_id, owner=franchise)
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    await animal.delete()
    return {"ok": True}


@router.post("/types", response_model=AnimalTypeOut, status_code=status.HTTP_201_CREATED)
async def create_animal_type(
    animal_type_in: AnimalTypeCreate,
    user: User = Depends(get_current_active_superuser)
):
    animal_type = await AnimalType.create(**animal_type_in.dict())
    return animal_type

@router.get("/types", response_model=List[AnimalTypeOut])
async def read_animal_types(
    skip: int = 0,
    limit: int = 100
):
    animal_types = await AnimalType.all().offset(skip).limit(limit)
    return animal_types

@router.get("/types/{type_id}", response_model=AnimalTypeOut)
async def read_animal_type(type_id: UUID4):
    animal_type = await AnimalType.get_or_none(id=type_id)
    if animal_type is None:
        raise HTTPException(status_code=404, detail="Animal type not found")
    return animal_type