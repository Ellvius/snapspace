from app.core.db import SessionLocal

# Dependency to provide a database session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db  # Synchronous generator
    finally:
        db.close()