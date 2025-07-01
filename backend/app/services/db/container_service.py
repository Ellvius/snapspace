from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.containers import Container
from app.schemas.container_schema import ContainerInsert, ContainerData

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
    
    try:
        db.add(new_container)
        db.commit()
        db.refresh(new_container)
        return  ContainerData.model_validate(new_container)
    except IntegrityError as e:
        db.rollback()
        raise ValueError(str(e))

