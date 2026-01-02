from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import GiftCardStatus


# ---------- User & Auth ----------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# ---------- Gift Cards ----------

class GiftCardBase(BaseModel):
    value: int  # in pence (e.g. 1000 = £10)
    currency: str = "GBP"


class GiftCardCreate(GiftCardBase):
    pass

class GiftCardCreated(BaseModel):
    id: int
    value: int
    currency: str
    code: str            # shown ONCE
    created_at: datetime

    class Config:
        from_attributes = True



class GiftCardOut(BaseModel):
    id: int
    value: int
    currency: str
    status: GiftCardStatus
    created_at: datetime
    redeemed_at: Optional[datetime]
    redeemed_by: Optional[str]

    class Config:
        from_attributes = True


class GiftCardStatusOut(BaseModel):
    status: GiftCardStatus
    value: int
    currency: str
    redeemed_by: Optional[str]
    redeemed_at: Optional[datetime]


class GiftCardRedeem(BaseModel):
    code: str

    model_config = {
        "from_attributes": True
    }



class RedeemRequest(BaseModel):
    code: str


class RedeemResponse(BaseModel):
    success: bool
    value: int
    currency: str
