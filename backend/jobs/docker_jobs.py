from app.core.docker_config import client
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def prune_container_less_networks() -> dict:
    deleted = []
    errors = []
    logger.info("Job started: prune unused networks.")
    try:
        networks = client.networks.list()
        logger.debug(f"Found {len(networks)} networks to inspect.")
        
        for network in networks:
            network.reload()
            containers = network.attrs.get("Containers", {})
            container_ids = list(containers.keys())
            
            if not container_ids:
                continue

            if len(container_ids) == 1:
                container_id = container_ids[0]
                
                try:
                    container = client.containers.get(container_id)
                    if container.name == settings.TRAEFIK_CONTAINER_NAME:
                        logger.info(f"Found unused network: {network.name}")
                        logger.info(f"Disconnecting {container.name} from network: {network.name}")
                        network.disconnect(container, force=True)
                        
                        logger.info(f"Removing unused network '{network.name}' (only connected to traefik).")
                        network.remove()
                        deleted.append(network.name)
                except Exception as e:
                    error_msg = f"Failed to inspect or remove network '{network.name}': {e}"
                    logger.warning(error_msg)
                    errors.append(error_msg)
    except Exception as e:
        error_msg = f"Failed to prune networks: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("Job completed: prune unused networks.")
    logger.debug(f"Deleted networks: {deleted}")
    return {
        "status": "success" if not errors else "partial",
        "deleted": deleted,
        "errors": errors
    }
    
    

