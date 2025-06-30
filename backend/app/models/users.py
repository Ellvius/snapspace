from sqlalchemy import Column, Integer, String
from app.core.db import Base
from app.schemas.user_schema import UserRoles

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String, index=True, unique=True)
    password = Column(String)
    role = Column(String, default=UserRoles.USER.value, nullable=False)