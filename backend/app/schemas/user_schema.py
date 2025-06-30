from pydantic import BaseModel, ConfigDict
from enum import Enum

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
