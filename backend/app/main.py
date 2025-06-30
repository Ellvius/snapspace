from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import environment, admin, user, auth
from app.core.db import Base, engine

# Initialize the Fastapi App with lifespan management
app = FastAPI(
    title="SnapSpace",
    root_path="/api"
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
app.include_router(auth.router)
app.include_router(environment.router)
app.include_router(admin.router)
app.include_router(user.router)

# Root route (for testing)
@app.get('/')
def read_root():
    return { "message" : "Dev Environment platform API"}