from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.core.db import Base
from app.schemas.user_schema import UserRoles

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) 
    username: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str] = mapped_column(String)
    role:Mapped[str] = mapped_column(String, default=UserRoles.USER.value, nullable=False)
    
    containers: Mapped[List["Container"]] = relationship( # type: ignore
        "Container",
        back_populates="owner",
        cascade="all, delete-orphan"
    )