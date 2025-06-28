from pydantic_settings import BaseSettings
from app.utils.paths import BASE_DIR

# Define a Settings class that extends BaseSettings for structured configuration
class Settings(BaseSettings):
    # Core DB config loaded from .env
    DATABASE_URL: str = "postgresql+psycopg2://user:password@db:5432/mydatabase"
    DEBUG: bool = False

    class Config:
        # Load environment variables from .env file
        env_file = BASE_DIR / '.env'
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()