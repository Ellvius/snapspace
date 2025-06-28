from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserOut
from app.core.dependencies import get_db
from app.services.user_services import create_user, get_all_users, get_user_by_username

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get("/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user