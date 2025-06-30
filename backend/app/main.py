from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import environment, admin, user, auth
from app.core.db import Base, engine
from app.config.settings import settings

# Initialize the Fastapi App with lifespan management
app = FastAPI(
    title=settings.PROJECT_TITLE,
    root_path=settings.API_ROOT
)

# Creates all tables defined in ORM models
Base.metadata.create_all(bind=engine)

# Enable CORS (Cross-Origin Resource Sharing) for all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(auth.router, prefix="/auth")
app.include_router(environment.router, prefix="/environments")
app.include_router(admin.router, prefix="/admin")
app.include_router(user.router, prefix="/users")

# Root route (for testing)
@app.get('/')
def read_root():
    return { "message" : "Dev Environment platform API"}