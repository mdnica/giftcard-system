from pydantic import BaseSettings


class Settings(BaseSettings):
    # security
    SECRET_KEY: str = "CHANGE_ME_TO_A_RANDOM_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # database
    DATABASE_URL: str = "sqlite:///./giftcards.db"

    # rate limiting
    MAX_REQUESTS_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
