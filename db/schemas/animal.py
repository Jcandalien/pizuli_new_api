from pydantic import BaseModel, UUID4
from typing import List, Optional
from db.models.animal import AnimalType
from db.schemas.meat import MeatImageOut
from db.schemas.product_attribute import ProductAttributeOut

class AnimalImageOut(BaseModel):
    id: UUID4
    image_url: str

    class Config:
        from_attributes = True


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
    images: Optional[List[AnimalImageOut]]
    attributes: Optional[List[ProductAttributeOut]]

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
    images: Optional[List[AnimalImageOut]]
    attributes: Optional[List[ProductAttributeOut]]


class AnimalOut(AnimalBase):
    id: UUID4
    owner_id: UUID4
    image: Optional[str]

    class Config:
        from_attributes = True