from pydantic import BaseModel, Field
from app.schemas.resource_profiles import ResourceProfile

class ContainerInput(BaseModel):
    image: str
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