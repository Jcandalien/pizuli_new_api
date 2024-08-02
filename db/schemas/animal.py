from pydantic import BaseModel, UUID4
from typing import Optional
from db.models.animal import AnimalType

class AnimalTypeBase(BaseModel):
    name: str

class AnimalTypeCreate(AnimalTypeBase):
    pass

class AnimalTypeUpdate(AnimalTypeBase):
    pass

class AnimalTypeOut(AnimalTypeBase):
    id: UUID4

    class Config:
        from_attributes = True

class AnimalBase(BaseModel):
    type_id: UUID4
    breed: str
    age: int
    weight: float
    health_status: str
    price: float
    quantity: int

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(BaseModel):
    type_id: Optional[UUID4] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    health_status: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class AnimalOut(AnimalBase):
    id: UUID4
    owner_id: UUID4
    image: Optional[str]

    class Config:
        from_attributes = True