from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.container_schema import ContainerInput, ContainerResponse, ContainerInfo, ContainerInsert, ContainerAction
from app.services.docker.container_service import (create_container, list_containers, restart_container, stop_container, pause_container, unpause_container, remove_container, get_container_logs)
from app.core.dependencies import get_current_user, required_roles
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRoles, UserOut
from app.utils.dock_net import get_new_dock_net
from app.config.resource_profiles import resource_profiles
from app.services.db.container_service import insert_container, update_container_status, delete_container, list_user_containers
from app.core.dependencies import get_db


router = APIRouter(tags=["Development Environments"])


@router.post("/", response_model=ContainerResponse)
def create_environment(env : ContainerInput, user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    env_network = get_new_dock_net()
    result = create_container(
        image_name=env.image, 
        network_name=env_network,
        subdomain=env.subdomain, 
        profile=env.profile
    )
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=result["message"]
        )
    
    data = result["container"]
    container_data = ContainerInsert(
        container_id=data["short_id"], # type: ignore
        name=data["name"], # type: ignore
        env=data["image"],   # type: ignore
        network=data["container_network"], # type: ignore
        pids_limit= resource_profiles[env.profile.value]["pids_limit"],
        owner_id=user.id,
        url= result["url"]
    )
    
    res = insert_container(container_data, db)

    if res is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error creating environment"
        )
    return res


@router.get("/", response_model=dict)
def list_environments(user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        containers = list_user_containers(user.id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    return {
        "status": "success",
        "message": "Containers fetched successfully",
        "container": containers
    }


@router.post("/{container_id}/{action}")
def control_environment(
    container_id: str, 
    action: ContainerAction,
    user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    match action:
        case ContainerAction.PAUSE:
            result = pause_container(container_id)
        case ContainerAction.UNPAUSE:
            result = unpause_container(container_id)
        case ContainerAction.STOP:
            result = stop_container(container_id)
        case ContainerAction.RESTART:
            result = restart_container(container_id)
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
        
    res = update_container_status(action, container_id, db)
    return result


@router.delete("/{container_id}", response_model=dict, status_code=status.HTTP_200_OK)
def delete_environment(
    container_id: str,
    user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # First, remove the actual Docker container
    result = remove_container(container_id)
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )

    # Then, delete the container record from the database
    try:
        container = delete_container(container_id, db)
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


@router.get("/{container_id}/logs", response_model=dict)
def fetch_logs(
    container_id: str, 
    tail: int = 100, 
    user: UserOut = Depends(get_current_user)
):
    result = get_container_logs(container_id, tail)
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )
    return result