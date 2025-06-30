from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from app.config.settings import settings
from app.models.users import User

# Setup bcrypt hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashes plain text password to secure bcrypt hash
def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)

# Checks if plain text password matches stored bcrypt hash
def verify_password(pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(pwd, hashed_pwd)


# Generates a JWT session token with user ID, username, and expiration
def generate_auth_token(data: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    payload = {
        "id": str(data.id),
        "username": data.username,
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)


# Verifies and decodes a JWT token
def verify_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except JWTError:
        raise ValueError("Invalid token")