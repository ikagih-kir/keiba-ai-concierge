from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Keiba Admin API"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
