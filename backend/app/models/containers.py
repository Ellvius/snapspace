from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.db import Base
from app.models.users import User
from app.config.settings import settings
from app.schemas.container_schema import ContainerStatus, Environments

class Container(Base):
    __tablename__ = "containers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False,unique=True, index=True)
    env = Column(SqlEnum(Environments), nullable=False)
    network = Column(String(100), nullable=False)
    status = Column(SqlEnum(ContainerStatus), nullable=False, default=ContainerStatus.RUNNING)
    mem_limit = Column(Integer, nullable=False, default=512)
    
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=text("CURRENT_TIMESTAMP")
    ) 
    
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )
    
    expire_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=settings.CONTAINER_LIFESPAN_HOURS),
        index=True
    )
    
    owner_id = Column(
        Integer, 
        ForeignKey(User.id, ondelete="CASCADE"), 
        nullable=False
    )
    
    # SQLAlchemy relationship for easy access to user data
    owner = relationship("User", back_populates="containers")