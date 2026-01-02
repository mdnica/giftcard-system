import secrets, hashlib
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from . import models, security
from .models import GiftCardStatus
from .utils import generate_giftcard_code
from .security import hash_giftcard_code


# ---------- Users ----------

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, email: str, password: str, is_admin: bool = False) -> models.User:
    hashed_pw = security.get_password_hash(password)
    user = models.User(email=email, hashed_password=hashed_pw, is_admin=is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- Gift Cards ----------

def get_giftcard_by_hash(db: Session, code_hash: str) -> Optional[models.GiftCard]:
    return (
    db.query(models.GiftCard)
    .filter(models.GiftCard.code_hash == code_hash)
    .first()
    )


def create_giftcard(db: Session, value: int, currency: str = "GBP"):
     plain_code = f"GC-{secrets.token_hex(6).upper()}"

     code_hash = hashlib.sha256(plain_code.encode()).hexdigest()

     giftcard = models.GiftCard(
        code_hash=code_hash,
        value=value,
        currency=currency
    )

     db.add(giftcard)
     db.commit()
     db.refresh(giftcard)

     return giftcard, plain_code


def list_giftcards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GiftCard).offset(skip).limit(limit).all()


def redeem_giftcard(db: Session, code: str):
    code_hash = hashlib.sha256(code.encode()).hexdigest()

    card = (
        db.query(models.GiftCard)
        .filter(models.GiftCard.code_hash == code_hash)
        .first()
    )

    if not card:
        return None, "INVALID_CODE"

    if card.status != GiftCardStatus.active:
        return None, "ALREADY_REDEEMED"

    card.status = GiftCardStatus.redeemed
    card.redeemed_at = datetime.utcnow()

    db.commit()
    db.refresh(card)

    return card, None



def increment_attempts(db: Session, card: models.GiftCard, ip: str, lock_threshold: int = 5):
    card.attempts += 1
    card.last_attempt_ip = ip
    if card.attempts >= lock_threshold and card.status == GiftCardStatus.active:
        card.status = GiftCardStatus.locked
    db.commit()
    db.refresh(card)
