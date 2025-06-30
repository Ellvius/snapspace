from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.auth_scheme import oauth2_scheme
from app.core.security import verify_token
from app.core.db import SessionLocal
from app.schemas.user_schema import UserRoles
from app.models.users import User
from app.services.user_services import get_user_by_id

# Dependency to provide a database session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db  # Synchronous generator
    finally:
        db.close()
        

# Dependency to get current user from token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except ValueError:
        raise credentials_exception
    
    user = get_user_by_id(user_id, db)
    if user is None:
        raise credentials_exception
    return user


def required_roles(*roles: UserRoles):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker