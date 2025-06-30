from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.users import User
from app.core.dependencies import get_db, get_current_user
from app.services.user_services import get_all_users

router = APIRouter(prefix="/users", tags=["User"])    
    
@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get("/me")
def get_user( current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return current_user