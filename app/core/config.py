from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "BookAI"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/bookdb"
    JWT_SECRET_KEY: str = "secrate key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24

    LLAMA_ENDPOINT: str = "http://host.docker.internal:11434/run"
    ADMIN_ROLE: str = "admin"
    USER_ROLE: str = "user"

    class Config:
        env_file = ".env"

settings = Settings()
