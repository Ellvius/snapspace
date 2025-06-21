from fastapi import APIRouter, HTTPException
from app.core.image_builder import build_all_templates
from app.utils.paths import TEMPLATE_DIR

router = APIRouter(prefix="/admin", tags=["Admin"])

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
        raise HTTPException(status_code=500, detail=f"Build failed: {e}")
        