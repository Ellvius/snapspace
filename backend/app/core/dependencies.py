from app.core.db import AsyncSessionLocal

# Dependency to provide a database session in FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session       # Yields a session for use in a request lifecycle
