from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.container_schema import ContainerInput, ContainerResponse, ContainerInfo, ContainerInsert, ContainerAction
from app.services.docker.container_service import (create_container, list_containers, restart_container, stop_container, pause_container, unpause_container, remove_container, get_container_logs)
from app.core.dependencies import get_current_user, required_roles
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRoles, UserOut
from app.utils.generate_name import generate_container_name, generate_unique_suffix, generate_network_name
from app.config.resource_profiles import resource_profiles
from app.services.db.container_service import insert_container, update_container_status, delete_container, list_user_containers, verify_container_access, enforce_pid_limit
from app.core.dependencies import get_db
from app.services.docker import network_service as dock_net


router = APIRouter(tags=["Development Environments"])


@router.post("/", response_model=dict)
def create_environment(
    env: ContainerInput, 
    user: UserOut = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Check if user's total pids would exceed MAX_PIDS
    env_pids = resource_profiles[env.profile]["pids_limit"]
    try:
        enforce_pid_limit(user.id, env_pids, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    # Create an isolated network and attach it to traefik
    container_network = generate_network_name()
    network = dock_net.create_isolated_network(container_network)
    dock_net.connect_traefik_to_network(container_network)
    # print(container_network)
    
    # Create a unique container name and env name
    container_name = generate_container_name()
    unique_hash = generate_unique_suffix()
    
    # Create Docker container
    result = create_container(
        container_name=container_name,
        image_name=env.image, 
        network_name=container_network,
        subdomain=f"{container_name}-{unique_hash}", 
        profile=env.profile
    )

    if result.get("status") == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=result["message"]
        )

    container_info = result["container"]
    container_data = ContainerInsert(
        container_id=container_info["short_id"], # type: ignore
        name=container_info["name"], # type: ignore
        env=container_info["image"], # type: ignore
        network=container_info["container_network"], # type: ignore
        pids_limit=resource_profiles[env.profile.value]["pids_limit"],
        owner_id=user.id,
        url=result["url"]
    )
    
    try:
        container = insert_container(container_data, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

    return {
        "status": "success",
        "message": "Container created successfully",
        "container": container,
        "url": result["url"]
    }


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
    try:
        res = verify_container_access(container_id, user.id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
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
    try:
        res = verify_container_access(container_id, user.id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    # First, remove the actual Docker container
    result = remove_container(container_id)
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )
        
    try:
        dock_net.delete_isolated_network(result["network"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        container = verify_container_access(container_id, user.id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
    result = get_container_logs(container_id, tail)
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=result["message"]
        )
    return result