from fastapi import APIRouter
from app.schemas.container_schema import ContainerInput, ContainerOutput
from app.services.docker_services import run_container, list_containers, stop_container

router = APIRouter(prefix="/environments", tags=["Development Environments"])

@router.post('/')
def create_environment(env : ContainerInput):
    return run_container(env.image)

@router.post('/{container_id}')
def stop_environment(container_id):
    return stop_container(container_id)

@router.get('/')
def list_environment():
    return list_containers()