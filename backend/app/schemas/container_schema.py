from pydantic import BaseModel, Field
from enum import Enum
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