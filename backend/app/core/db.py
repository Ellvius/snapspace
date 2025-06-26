from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config.settings import settings

# Ensure the correct async PostgreSQL driver is used
if not settings.DATABASE_URL.startswith("postgresql+asyncpg://"):
    raise ValueError(
        "Async mode requires PostgreSQL with asyncpg. "
        f"Got: {settings.DATABASE_URL}"
    )
    
    
# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,     # Check if connection is alive before usin
    pool_size=20,           # Max number of persistent connections
    max_overflow=10,        # Extra connections allowed temporarily
    echo=settings.DEBUG     # Log SQL queries if DEBUG=True
)


# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # Keep objects active after commit
    autoflush=False             # Manual flushing preferred in async context
)


# Base class for ORM models
Base = declarative_base()

