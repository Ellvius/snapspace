from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.containers import Container
from app.config.settings import settings
from app.schemas.container_schema import ContainerInsert, ContainerData, ContainerAction, ContainerStatus

def get_container_by_id(container_id: str, db: Session) -> Container | None:
    return db.query(Container).filter(Container.container_id == container_id).first()


def insert_container(container_data: ContainerInsert, db: Session) -> ContainerData:
    new_container = Container(
        container_id = container_data.container_id,
        name = container_data.name,
        env = container_data.env,
        network = container_data.network,
        pids_limit = container_data.pids_limit,
        owner_id = container_data.owner_id,
        url = container_data.url
    )
    
    if not new_container:
        raise ValueError("Could not create container in db")
    
    try:
        db.add(new_container)
        db.commit()
        db.refresh(new_container)
        return  ContainerData.model_validate(new_container)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to insert the container in db: {str(e)}")


def update_container_status(action: ContainerAction, container_id: str, db: Session) -> ContainerData:
    # Define the mapping from action to status
    action_to_status = {
        ContainerAction.UNPAUSE: ContainerStatus.RUNNING,
        ContainerAction.RESTART: ContainerStatus.RUNNING,
        ContainerAction.PAUSE: ContainerStatus.PAUSED,
        ContainerAction.STOP: ContainerStatus.EXITED,
    }

    if action not in action_to_status:
        raise ValueError("Invalid container action")

    container = get_container_by_id(container_id, db)
    if not container:
        raise ValueError("Container not found")

    try:
        container.status = action_to_status[action]
        db.commit()
        db.refresh(container)
        return ContainerData.model_validate(container)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update status: {e}")


def delete_container(id: str, db: Session) -> ContainerData:
    container = get_container_by_id(id, db)
    if not container:
        raise ValueError("Container not found")

    try:
        db.delete(container)
        db.commit()
        return ContainerData.model_validate(container)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete container: {e}")
    
    
def list_user_containers(user_id: int, db: Session) -> List[ContainerData]:
    try:
        containers = (
            db.query(Container)
            .filter(Container.owner_id == user_id)
            .all()
        )
        return [
            ContainerData.model_validate(c) for c in containers
        ]
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to fetch user containers: {e}")
    
    

def verify_container_access(container_id: str, user_id: int, db: Session) -> Container:
    container = get_container_by_id(container_id, db)
    if not container:
        raise ValueError("Container not found")
    if container.owner_id != user_id:
        raise PermissionError("User does not own this container")
    return container


def enforce_pid_limit(user_id: int, new_pids: int, db: Session):
    current_total = (
        db.query(func.sum(Container.pids_limit))
        .filter(Container.owner_id == user_id).scalar() or 0
    )
    
    if current_total + new_pids > settings.MAX_PIDS:
        raise ValueError(f"PID limit exceeded. Current: {current_total}, Requested: {new_pids}, Max: {settings.MAX_PIDS}, Try deleting existing environments.")
    

def get_container_info(container_id: str, db: Session) -> ContainerData | None:
    container = get_container_by_id(container_id, db)
    if not container:
        raise ValueError("Container not found")
    
    return ContainerData.model_validate(container)


def get_all_containers(db: Session) -> List[ContainerData]:
    try:
        containers = db.query(Container).order_by(Container.created_at.desc()).all()
        return [
            ContainerData.model_validate(c) for c in containers
        ]
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to fetch containers: {e}")
    
    
def delete_container_network(network_name: str | None, db: Session) -> ContainerData:
    if not network_name:
        raise ValueError("Network name must be provided.")
    
    # Search for the container having the network
    container = db.query(Container).filter(Container.network == network_name).first()
    if not container:
        raise ValueError(f"Container with network {network_name} not found.")
    
    try:
        # Delete the container entry with the given network
        db.delete(container)
        db.commit()
        return ContainerData.model_validate(container)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete container network {network_name}: {e}")