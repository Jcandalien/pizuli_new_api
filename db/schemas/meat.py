from db.schemas.product_attribute import ProductAttributeOut
from pydantic import BaseModel, UUID4
from typing import Optional, List

class MeatTypeBase(BaseModel):
    name: str

class MeatTypeCreate(MeatTypeBase):
    pass

class MeatTypeUpdate(MeatTypeBase):
    pass

class MeatTypeOut(MeatTypeBase):
    id: UUID4

    class Config:
        from_attributes = True

class MeatImageOut(BaseModel):
    id: UUID4
    image_url: str

    class Config:
        from_attributes = True

class MeatCreate(BaseModel):
    type_id: UUID4
    cut: str
    grade: str
    weight: float
    price: float
    is_frozen: Optional[bool] = False
    is_fresh: Optional[bool] = True
    stock_quantity: int
    tag_ids: Optional[List[UUID4]] = []
    images: Optional[List[MeatImageOut]]
    attributes: Optional[List[ProductAttributeOut]]

class MeatUpdate(BaseModel):
    type_id: Optional[UUID4] = None
    cut: Optional[str] = None
    grade: Optional[str] = None
    weight: Optional[float] = None
    price: Optional[float] = None
    is_frozen: Optional[bool] = None
    is_fresh: Optional[bool] = None
    stock_quantity: Optional[int] = None
    image: Optional[str] = None
    tag_ids: Optional[List[UUID4]] = []
    images: Optional[List[MeatImageOut]]
    attributes: Optional[List[ProductAttributeOut]]



class MeatOut(BaseModel):
    id: UUID4
    type_id: UUID4
    cut: str
    grade: str
    weight: float
    price: float
    is_frozen: bool
    is_fresh: bool
    stock_quantity: int
    image: Optional[str]
    tag_ids: List[UUID4]
    is_chilled: bool
    images: Optional[List[MeatImageOut]]
    attributes: Optional[List[ProductAttributeOut]]

    class Config:
        from_attributes = True