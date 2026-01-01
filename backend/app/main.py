from app.database import engine
from app import models
from fastapi import FastAPI
from app.api import auth, giftcards


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(giftcards.router)
