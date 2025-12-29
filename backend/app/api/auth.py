from fastapi import APIRouter, Depends

from ..dependencies import login_for_access_token
from ..schemas import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
def login(token: Token = Depends(login_for_access_token)):
    return token
