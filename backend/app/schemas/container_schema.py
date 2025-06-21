from pydantic import BaseModel

class ContainerInput(BaseModel):
    image: str
    
    
class ContainerOutput(BaseModel):
    id: str
    short_id: str
    name: str
    image: str
    status: str