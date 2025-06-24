from pydantic import BaseModel

class ContainerInput(BaseModel):
    image: str
    subdomain: str
    
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