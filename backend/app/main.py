from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import environment, admin, user, auth
from app.core.db import Base, engine
from app.config.settings import settings
from app.core.admin_setup import create_admin
from app.utils.logger import setup_logger
from jobs import scheduler as sched

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database Tables Intialized.")
        create_admin()
        logger.info("Admin user created.")
        sched.start_scheduler()
    except Exception as e:
        logger.exception("Startup failed during initialization.")
        raise
    yield
    sched.shutdown_scheduler()
    logger.info("Shutdown complete: Scheduler stopped.")


# Initialize the Fastapi App with lifespan management
app = FastAPI(
    title=settings.PROJECT_TITLE,
    root_path=settings.API_ROOT,
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
app.include_router(auth.router, prefix="/auth")
app.include_router(environment.router, prefix="/environments")
app.include_router(admin.router, prefix="/admin")
app.include_router(user.router, prefix="/users")

# Root route (for testing)
@app.get('/')
def read_root():
    return { "message" : "Dev Environment platform API"}