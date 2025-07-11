from typing import List
from pydantic import BaseModel, ConfigDict
from enum import Enum
from app.schemas.container_schema import ContainerData

class UserRoles(str, Enum):
    USER = "user"
    ADMIN = "admin"
    

class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UserWithContainers(BaseModel):
    id: int
    username: str
    role: str
    containers: List[ContainerData] = []

    model_config = ConfigDict(from_attributes=True)
