from sqlalchemy import TIMESTAMP, ForeignKey, String, Integer, text, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, timedelta
from app.core.db import Base
from app.config.settings import settings
from app.schemas.container_schema import ContainerStatus, Environments

class Container(Base):
    __tablename__ = "containers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    container_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    env: Mapped[Environments] = mapped_column(SqlEnum(Environments), nullable=False)
    network: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[ContainerStatus] = mapped_column(
        SqlEnum(ContainerStatus), nullable=False, default=ContainerStatus.RUNNING
    )
    pids_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    expire_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=settings.CONTAINER_LIFESPAN_HOURS),
        index=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Relationship to User model
    owner: Mapped["User"] = relationship("User", back_populates="containers") # type: ignore
