from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.services.docker.image_service import build_all_templates
from app.services.docker import container_service as docker_svc
from app.services.docker.network_service import delete_isolated_network
from app.services.db.user_services import get_all_users, get_user_with_containers, delete_user_by_id
from app.services.db import container_service as cont_svc
from app.utils.paths import TEMPLATE_DIR
from app.core.dependencies import required_roles, get_db
from app.schemas.user_schema import UserRoles
from app.schemas.container_schema import ContainerAction
from jobs.docker_jobs import prune_container_less_networks

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
    
    
@router.get("/docker_containers", response_model=dict)
def list_all_docker_containers():
    result = docker_svc.list_containers()

    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )

    return {
        "status": "success",
        "containers": result["containers"]
    }
    
    
@router.get("/containers", response_model=dict)
def list_all_containers(db: Session = Depends(get_db)):
    try:
        containers = cont_svc.get_all_containers(db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    return {
        "message": "successfully fetched container info",
        "container": containers
    }
    


@router.get("/containers/{container_id}", response_model=dict)
def get_container_detail(container_id: str, db: Session = Depends(get_db)):
    try:
        container = cont_svc.get_container_info(container_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    return {
        "message": "successfully fetched container info",
        "container": container
    }
    
    
@router.post("/containers/{container_id}/{action}")
def control_environment(container_id: str, action: ContainerAction, db: Session = Depends(get_db)):
    match action:
        case ContainerAction.PAUSE:
            result = docker_svc.pause_container(container_id)
        case ContainerAction.UNPAUSE:
            result = docker_svc.unpause_container(container_id)
        case ContainerAction.STOP:
            result = docker_svc.stop_container(container_id)
        case ContainerAction.RESTART:
            result = docker_svc.restart_container(container_id)
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Unsupported action"
            )

    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=result["message"]
        )
    
    try:
        res = cont_svc.update_container_status(action, container_id, db)
        
        return {
            "status": "success",
             "message": f"Container '{container_id}' status updated to '{res.status}'",
            "container": res
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        

@router.delete("/containers/{container_id}", response_model=dict, status_code=status.HTTP_200_OK)
def delete_environment(container_id: str, db: Session = Depends(get_db)):
    # First, remove the actual Docker container
    result = docker_svc.remove_container(container_id)
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )
        
    try:
        delete_isolated_network(result["network"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Then, delete the container record from the database
    try:
        container = cont_svc.delete_container(container_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    return {
        "status": "success",
        "message": f"Container '{container_id}' deleted successfully",
        "container": container
    }


@router.get("/containers/{container_id}/logs", response_model=dict)
def fetch_logs(container_id: str, tail: int = 100):
    result = docker_svc.get_container_logs(container_id, tail)
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )
    return result


@router.post("/prune-networks")
def manual_network_prune():
    try:
        result = prune_container_less_networks()
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
