from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from app.schemas.resource_profiles import ResourceProfile

class Environments(str, Enum):
    PYTHON = "python-env"
    NODE = "nodejs-env"
    

class ContainerInput(BaseModel):
    image: Environments = Field(
        default=Environments.PYTHON,
        description="Pre-configured development environments"
    )
    subdomain: str
    profile: ResourceProfile = Field(
        default=ResourceProfile.LOW,
        description="Resource profile tier: low, medium, or high"
    )
    
class ContainerInfo(BaseModel):
    id: str
    short_id: str
    name: str
    image: str
    network: str | None = None
    status: str | None = None
    
    
class ContainerResponse(BaseModel):
    status: str
    message: str | None = None
    container: ContainerInfo | None = None
    url: str | None = None
    

class ContainerAction(str, Enum):
    PAUSE = "pause"
    UNPAUSE = "unpause"
    STOP = "stop"
    RESTART = "restart"  
    

class ContainerStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    RESTARTING = "restarting"
    EXITED = "exited"
    DEAD = "dead"
    
    
# DATABASE CRUD SCHEMAS 
    
class BaseContainer(BaseModel):
    container_id: str 
    name: str
    env: Environments
    network: str
    pids_limit: int | None = None
    url: str

class ContainerInsert(BaseContainer):
    owner_id: int

class ContainerData(BaseContainer):
    id: int
    status: ContainerStatus
    created_at: datetime
    updated_at: datetime
    expire_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
