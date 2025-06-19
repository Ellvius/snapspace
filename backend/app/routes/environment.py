from fastapi import APIRouter

router = APIRouter(prefix="/environments", tags=["Development Environments"])

@router.post('/')
def create_environment():
    # Create a new development environment
    return {"status" : "successfully created environment"}

@router.get('/')
def list_environment():
    # Get all the available environments
    return {"status": "list of environments available"}