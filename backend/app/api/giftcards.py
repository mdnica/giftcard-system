from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import hashlib
import secrets

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_admin_user, get_current_user
from ..models import GiftCardStatus

router = APIRouter(prefix="/giftcards", tags=["Gift Cards"])


# ---------- Admin Routes ----------

@router.post("/", response_model=schemas.GiftCardOut)
def create_giftcard(
    giftcard: schemas.GiftCardCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    # Generate a secure random gift card code (shown once)
    raw_code = f"GC-{secrets.token_hex(6).upper()}"

    # Store only the hash
    code_hash = hashlib.sha256(raw_code.encode()).hexdigest()

    card = crud.create_giftcard(
        db=db,
        code_hash=code_hash,
        value=giftcard.value,
        currency=giftcard.currency,
    )

    # NOTE: In real apps you return raw_code ONCE to admin
    return card


@router.get("/", response_model=list[schemas.GiftCardOut])
def list_giftcards(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    return crud.list_giftcards(db)


# ---------- User Routes ----------

@router.post("/redeem", response_model=schemas.RedeemResponse)
def redeem_giftcard(
    request: Request,
    payload: schemas.RedeemRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    code_hash = hashlib.sha256(payload.code.encode()).hexdigest()
    card = crud.get_giftcard_by_hash(db, code_hash)

    if not card:
        raise HTTPException(status_code=404, detail="Gift card not found")

    if card.status != GiftCardStatus.active:
        crud.increment_attempts(db, card, request.client.host)
        raise HTTPException(status_code=400, detail="Gift card not redeemable")

    card = crud.redeem_giftcard(db, card, user.email)

    return schemas.RedeemResponse(
        success=True,
        value=card.value,
        currency=card.currency,
    )
