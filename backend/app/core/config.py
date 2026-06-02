from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://stellara:stellara@db:5432/stellara"

    class Config:
        env_file = ".env"


settings = Settings()
