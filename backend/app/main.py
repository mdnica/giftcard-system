from fastapi import FastAPI
from app.api import auth, giftcards

app = FastAPI()

app.include_router(auth.router)
app.include_router(giftcards.router)
