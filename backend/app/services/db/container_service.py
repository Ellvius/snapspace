from sqlalchemy.orm import Session
from app.models.containers import Container
from app.schemas.container_schema import ContainerInsert, ContainerData, ContainerAction, ContainerStatus

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

    container = db.query(Container).filter(Container.container_id == container_id).first()
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
    container = db.query(Container).filter(Container.container_id == id).first()
    if not container:
        raise ValueError("Container not found")

    try:
        db.delete(container)
        db.commit()
        return ContainerData.model_validate(container)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete container: {e}")
    
    