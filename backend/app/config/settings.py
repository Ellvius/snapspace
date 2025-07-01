from pydantic_settings import BaseSettings
from app.utils.paths import BASE_DIR

# Define a Settings class that extends BaseSettings for structured configuration
class Settings(BaseSettings):
    # Project configs
    PROJECT_TITLE: str = "snapspace"
    API_ROOT: str = "/api"
    
    # Admin Credentials
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "1234"
    
    # Core DB config loaded from .env
    DATABASE_URL: str = "postgresql+psycopg2://user:password@db:5432/mydatabase"
    DEBUG: bool = False
    
    # JWT config 
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 6 
    
    CONTAINER_LIFESPAN_HOURS: int = 3

    class Config:
        # Load environment variables from .env file
        env_file = BASE_DIR / '.env'
        env_file_encoding = "utf-8"
        extra = "forbid" # Raise error on extra fields in .env


# Global settings instance
settings = Settings()