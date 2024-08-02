from pydantic import BaseModel, UUID4
from typing import Optional
from db.models.franchise import FranchiseType

class FranchiseBase(BaseModel):
    name: str
    type: FranchiseType
    location: str
    description: str

class FranchiseCreate(FranchiseBase):
    pass

class FranchiseUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[FranchiseType] = None
    location: Optional[str] = None
    description: Optional[str] = None

class FranchiseOut(FranchiseBase):
    id: UUID4
    owner_id: UUID4
    rating: float
    review_count: int
    is_approved: bool

    class Config:
        from_attributes = True