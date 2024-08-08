from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import UUID4
from api.deps import get_approved_franchise, get_current_active_superuser
from db.models.franchise import Franchise
from db.models.meat import Meat, MeatType
from db.schemas.meat import MeatCreate, MeatOut, MeatUpdate, MeatTypeCreate, MeatTypeOut
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[MeatOut])
async def read_meats(
    skip: int = 0,
    limit: int = 100,
    meat_type_id: Optional[UUID4] = Query(None),
    cut: Optional[str] = Query(None),
    grade: Optional[str] = Query(None),
    is_frozen: Optional[bool] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None)
):
    query = Meat.all()
    if meat_type_id:
        query = query.filter(type_id=meat_type_id)
    if cut:
        query = query.filter(cut=cut)
    if grade:
        query = query.filter(grade=grade)
    if is_frozen is not None:
        query = query.filter(is_frozen=is_frozen)
    if min_price is not None:
        query = query.filter(price__gte=min_price)
    if max_price is not None:
        query = query.filter(price__lte=max_price)

    meats = await query.offset(skip).limit(limit)
    return meats



@router.post("/", response_model=MeatOut, status_code=status.HTTP_201_CREATED)
async def create_meat(
    meat_in: MeatCreate,
    franchise: Franchise = Depends(get_approved_franchise)
):
    meat_type = await MeatType.get_or_none(id=meat_in.type_id)
    if not meat_type:
        raise HTTPException(status_code=404, detail="Meat type not found")

    meat = await Meat.create(**meat_in.dict(), franchise=franchise, type=meat_type)
    return meat

@router.get("/{meat_id}", response_model=MeatOut)
async def read_meat(meat_id: UUID4):
    meat = await Meat.get_or_none(id=meat_id).prefetch_related("images", "attributes")
    if meat is None:
        raise HTTPException(status_code=404, detail="Meat not found")
    return meat


@router.put("/{meat_id}", response_model=MeatOut)
async def update_meat(
    meat_id: UUID4,
    meat_in: MeatUpdate,
    franchise: Franchise = Depends(get_approved_franchise)
):
    meat = await Meat.get_or_none(id=meat_id, franchise=franchise)
    if meat is None:
        raise HTTPException(status_code=404, detail="Meat not found")

    meat_data = meat_in.dict(exclude_unset=True)
    for field, value in meat_data.items():
        setattr(meat, field, value)
    await meat.save()
    return meat




@router.delete("/{meat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meat(
    meat_id: UUID4,
    franchise: Franchise = Depends(get_approved_franchise)
):
    meat = await Meat.get_or_none(id=meat_id, franchise=franchise)
    if meat is None:
        raise HTTPException(status_code=404, detail="Meat not found")
    await meat.delete()
    return {"ok": True}


# endpoints for managing MeatTypes (only accessible by superusers)
@router.post("/types", response_model=MeatTypeOut, status_code=status.HTTP_201_CREATED)
async def create_meat_type(
    meat_type_in: MeatTypeCreate,
    _: Franchise = Depends(get_current_active_superuser)
):
    meat_type = await MeatType.create(**meat_type_in.dict())
    return meat_type

@router.get("/types", response_model=List[MeatTypeOut])
async def read_meat_types(
    skip: int = 0,
    limit: int = 100
):
    meat_types = await MeatType.all().offset(skip).limit(limit)
    return meat_types