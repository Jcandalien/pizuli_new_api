from pydantic import BaseModel, EmailStr, UUID4


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID4
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class UserEdit(BaseModel):
    fullname: str
    username: str
    email: str
    phone_number: str