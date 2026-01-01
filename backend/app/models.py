from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from .database import Base
import enum


class GiftCardStatus(str, enum.Enum):
    active = "active"
    redeemed = "redeemed"
    locked = "locked"
    expired = "expired"


class GiftCard(Base):
    __tablename__ = "giftcards"

    id = Column(Integer, primary_key=True, index=True)
    code_hash = Column(String, unique=True, index=True, nullable=False)
    value = Column(Integer, nullable=False)  # in smallest currency unit, e.g. pence
    currency = Column(String, default="GBP", nullable=False)
    status = Column(Enum(GiftCardStatus), default=GiftCardStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    redeemed_at = Column(DateTime(timezone=True), nullable=True)
    redeemed_by = Column(String, nullable=True)
s    attempts = Column(Integer, default=0)
    last_attempt_ip = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
