from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import environment, admin
from app.core.db import Base, engine
from sqlalchemy import text


# Define the application's lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            print(f"✅ PostgreSQL connected! Version: {result.scalar()}")
            await conn.run_sync(Base.metadata.create_all)
            print("📦 Tables ensured.")
    except Exception as e:
        print(f"❌ Failed to connect to DB: {e}")
        raise   # Prevent app from starting if DB connection fails
    
    yield   # This allows the app to start and serve requests
    
    # Shutdown (if needed)
    print("Shutting down...")


# Initialize the Fastapi App with lifespan management
app = FastAPI(
    title="SnapSpace",
    root_path="/api",
    lifespan=lifespan
)


# Enable CORS (Cross-Origin Resource Sharing) for all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(environment.router)
app.include_router(admin.router)

# Root route (for testing)
@app.get('/')
def read_root():
    return { "message" : "Dev Environment platform API"}