from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.services.docker.image_service import build_all_templates
from app.services.db.user_services import get_all_users, get_user_with_containers, delete_user_by_id
from app.utils.paths import TEMPLATE_DIR
from app.core.dependencies import required_roles, get_db
from app.schemas.user_schema import UserRoles

router = APIRouter(
    tags=["Admin"],
    dependencies=[Depends(required_roles(UserRoles.ADMIN))]
)

@router.post("/build-images")
def build_images():
    print("Building all environments")
    try:
        images = build_all_templates(str(TEMPLATE_DIR))
        return {
            "status": "success",
            "built_images": images 
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Build failed: {e}"
        )
        
        
@router.get("/users", response_model=dict)
def list_all_users(db: Session = Depends(get_db)):
    try:
        users = get_all_users(db)
        return {
            "users": users
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users : {e}"   
        )
        

@router.get("/users/{user_id}", response_model=dict)
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    user = get_user_with_containers(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return {
        "user": user
    }


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = delete_user_by_id(user_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return {
        "status": "success",
        "message": f"User {user_id} deleted successfully",
        "user": user
    }