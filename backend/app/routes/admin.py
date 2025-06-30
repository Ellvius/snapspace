from fastapi import APIRouter, HTTPException, status, Depends
from app.services.docker.image_service import build_all_templates
from app.utils.paths import TEMPLATE_DIR
from app.core.dependencies import required_roles
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
        