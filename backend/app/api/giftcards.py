from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import hashlib
import secrets

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_admin_user, get_current_user
from ..models import GiftCardStatus
from app import models 

router = APIRouter(prefix="/giftcards", tags=["Gift Cards"])


# ---------- Admin Routes ----------

@router.post("/", response_model=schemas.GiftCardCreated)
def create_giftcard(
   
    payload: schemas.GiftCardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user),
): 

    giftcard, plain_code = crud.create_giftcard(
        db,
        value=payload.value,
        currency=payload.currency,
    )
    return {
        "id": giftcard.id,
        "value": giftcard.value,
        "currency": giftcard.currency,
        "code": plain_code,              # 👈 visible ONCE
        "created_at": giftcard.created_at,
    }


@router.get("/", response_model=list[schemas.GiftCardOut])
def list_giftcards(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    return crud.list_giftcards(db)


# ---------- User Routes ----------

@router.post("/redeem")
def redeem_giftcard(
    payload: schemas.GiftCardRedeem,
    request: Request,
    db: Session = Depends(get_db),
):
    client_ip = request.client.host

    card, error = crud.redeem_giftcard(db, payload.code, client_ip)

    if error == "INVALID_CODE":
        raise HTTPException(status_code=404, detail="Invalid gift card")

    if error == "LOCKED":
        raise HTTPException(
            status_code=403,
            detail="Gift card locked due to too many failed attempts"
        )

    if error == "ALREADY_REDEEMED":
        raise HTTPException(
            status_code=400,
            detail="Gift card already redeemed"
        )

    return {
        "message": "Gift card redeemed successfully",
        "value": card.value,
        "currency": card.currency,
    }
