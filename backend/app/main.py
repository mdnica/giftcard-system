from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models
from app.api import auth, giftcards
from app.middleware.rate_limit import RateLimitMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1️⃣ CORS middleware (for frontend / browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # demo / YouTube
    allow_credentials=True,
    allow_methods=["*"],          # allows OPTIONS
    allow_headers=["*"],
)

# 2️⃣ Rate limiting middleware (custom)
app.add_middleware(
    RateLimitMiddleware,
)

# Routers
app.include_router(auth.router)
app.include_router(giftcards.router)
