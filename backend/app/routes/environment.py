from fastapi import APIRouter, HTTPException
from app.schemas.container_schema import ContainerInput, ContainerResponse, ContainerInfo
from app.services.docker_services import (create_container, list_containers, restart_container, remove_container, get_container_logs)
from app.utils.dock_net import get_new_dock_net


router = APIRouter(prefix="/environments", tags=["Development Environments"])


@router.post("/", response_model=ContainerResponse)
def create_environment(env : ContainerInput):
    env_network = get_new_dock_net()
    result = create_container(env.image, env_network)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.get("/", response_model=list[ContainerInfo])
def list_environments():
    result = list_containers()
    if isinstance(result, dict) and result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result["containers"]


@router.put("/{container_id}", response_model=dict)
def restart_environment(container_id: str):
    result = restart_container(container_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.delete("/{container_id}", response_model=dict)
def delete_environment(container_id: str):
    result = remove_container(container_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.get("/{container_id}/logs", response_model=dict)
def fetch_logs(container_id: str, tail: int = 100):
    result = get_container_logs(container_id, tail)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result