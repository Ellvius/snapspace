from app.core.docker_config import client
from app.config.settings import settings
from app.utils.logger import setup_logger
from app.services.db.container_service import delete_container_network
from sqlalchemy.orm import Session
from app.core.db import SessionLocal

logger = setup_logger(__name__)

def prune_container_less_networks() -> dict:
    db: Session = SessionLocal()
    deleted = []
    errors = []
    
    logger.info("Job started: prune unused networks.")
    
    try:
        networks = client.networks.list()
        logger.debug(f"Found {len(networks)} networks to inspect.")
        
        for network in networks:
            connected_containers = client.containers.list(all=True, filters={"network": network.name})
            
            logger.debug([c.name for c in connected_containers])
            if len(connected_containers) != 1:
                continue  # Not an isolated traefik-only network

            container = connected_containers[0]
            container.reload()
            
            if container.name == settings.TRAEFIK_CONTAINER_NAME and container.status == "running":
                logger.info(f"Found unused network: {network.name}")
                
                try:
                    # Disconnect Traefik 
                    logger.info(f"Disconnecting {container.name} from network: {network.name}")
                    network.disconnect(container, force=True)
                    
                    # Remove the network 
                    logger.info(f"Removing unused network '{network.name}' (only connected to traefik).")
                    network.remove()
                    
                    # Delete from DB if tracked
                    logger.debug(f"Deleting DB entry for network: '{network.name}'")
                    delete_container_network(network.name, db)
                    
                    deleted.append(network.name)
                    
                except Exception as e:
                    error_msg = f"Failed to inspect or remove network '{network.name}': {e}"
                    logger.warning(error_msg)
                    errors.append(error_msg)
                
    except Exception as e:
        msg = f"Failed to prune networks: {e}"
        logger.exception(msg)
        raise ValueError(msg)
    finally:
        db.close()
        
    logger.info("Job completed: prune unused networks.")
    logger.debug(f"Deleted networks: {deleted}")
    return {
        "status": "success" if not errors else "partial",
        "deleted": deleted,
        "errors": errors
    }
    
    

