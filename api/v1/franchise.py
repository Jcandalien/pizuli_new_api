from fastapi import APIRouter, Depends, HTTPException, status, Query
from db.models.franchise import Franchise, FranchiseType
from db.schemas.franchise import FranchiseCreate, FranchiseUpdate, FranchiseOut
from api.deps import get_current_active_user
from db.models.user import User
from typing import List, Optional
from tortoise.expressions import Q
from pydantic import UUID4

router = APIRouter()

@router.post("/", response_model=FranchiseOut)
async def create_franchise(
    franchise_in: FranchiseCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new franchise.
    """
    franchise = await Franchise.create(**franchise_in.dict(), owner=current_user)
    return franchise


@router.get(
    "/",
    response_model=List[FranchiseOut],
    summary="List Franchises",
    description="Retrieve a list of franchises with optional filtering and search capabilities.",
    openapi_extra={
        "examples": {
            "Simple": {
                "summary": "Simple request",
                "value": {"skip": 0, "limit": 10}
            },
            "With Search": {
                "summary": "Search for 'burger'",
                "value": {"skip": 0, "limit": 10, "search": "burger"}
            },
            "Filtered": {
                "summary": "Filter by type and rating",
                "value": {"skip": 0, "limit": 10, "franchise_type": FranchiseType.RESTAURANT, "min_rating": 4.0}
            }
        }
    }
)
async def read_franchises(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return"),
    search: Optional[str] = Query(None, min_length=3, max_length=50, description="Search term for name or description"),
    franchise_type: Optional[FranchiseType] = Query(None, description="Filter by franchise type"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    max_rating: Optional[float] = Query(None, ge=0, le=5, description="Maximum rating")
):
    """
    Retrieve a list of franchises.

    - **skip**: Number of records to skip (pagination)
    - **limit**: Number of records to return (pagination)
    - **search**: Optional search term to filter franchises by name or description
    - **franchise_type**: Optional filter for specific franchise types
    - **min_rating**: Optional filter for minimum franchise rating
    - **max_rating**: Optional filter for maximum franchise rating

    Returns a list of franchises matching the specified criteria.
    """
    query = Franchise.all()

    if search:
        query = query.filter(Q(name__icontains=search) | Q(description__icontains=search))

    if franchise_type:
        query = query.filter(type=franchise_type)

    if min_rating is not None:
        query = query.filter(rating__gte=min_rating)

    if max_rating is not None:
        query = query.filter(rating__lte=max_rating)

    franchises = await query.offset(skip).limit(limit)
    return franchises


@router.get("/{franchise_id}", response_model=FranchiseOut)
async def read_franchise(franchise_id: int):
    """
    Get a specific franchise by ID.
    """
    franchise = await Franchise.get_or_none(id=franchise_id)
    if franchise is None:
        raise HTTPException(status_code=404, detail="Franchise not found")
    return franchise


@router.put("/{franchise_id}", response_model=FranchiseOut)
async def update_franchise(
    franchise_id: int,
    franchise_in: FranchiseUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a franchise.
    """
    franchise = await Franchise.get_or_none(id=franchise_id, owner=current_user)
    if franchise is None:
        raise HTTPException(status_code=404, detail="Franchise not found")

    franchise_data = franchise_in.dict(exclude_unset=True)
    for field, value in franchise_data.items():
        setattr(franchise, field, value)
    await franchise.save()
    return franchise


@router.delete("/{franchise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_franchise(
    franchise_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a franchise.
    """
    franchise = await Franchise.get_or_none(id=franchise_id, owner=current_user)
    if franchise is None:
        raise HTTPException(status_code=404, detail="Franchise not found")
    await franchise.delete()
    return {"ok": True}


@router.post("/{franchise_id}/pause", response_model=FranchiseOut)
async def pause_franchise(
    franchise_id: UUID4,
    pause: bool,
    current_user: User = Depends(get_current_active_user)
):
    franchise = await Franchise.get_or_none(id=franchise_id, owner=current_user)
    if not franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")

    franchise.is_paused = pause
    await franchise.save()
    return franchise