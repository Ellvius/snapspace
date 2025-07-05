from apscheduler.schedulers.background import BackgroundScheduler
from jobs.docker_jobs import prune_container_less_networks
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


scheduler = BackgroundScheduler()

def start_scheduler():
    # Register all jobs here
    scheduler.add_job(prune_container_less_networks, "interval", minutes=30)
    scheduler.start()
    logger.info("Scheduler started successfully")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shut down successfully.")