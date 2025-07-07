from docker.errors import NotFound, APIError
from docker.models.networks import Network
from app.core.docker_config import client
from app.config.settings import settings

def create_isolated_network(network_name: str) -> Network:
    return client.networks.create(
        name=network_name,
        driver="bridge",
        attachable=True
    )

def connect_traefik_to_network(network_name: str, traefik_container_name: str = f"{settings.PROJECT_TITLE}-traefik"):
    try:
        network = client.networks.get(network_name)
        container = client.containers.get(traefik_container_name)
        network.connect(container)
    except Exception as e:
        raise RuntimeError(f"Failed to connect Traefik to network '{network_name}': {e}")


def delete_isolated_network(network_name: str) -> None:
    try:
        network = client.networks.get(network_name)
        connected_containers = network.attrs.get("Containers", {})

        for container_id in connected_containers or {}:
            try:
                network.disconnect(container_id, force=True)
            except Exception as e:
                raise RuntimeError(f"Failed to disconnect container '{container_id}' from network '{network_name}': {e}")

        network.remove()

    except NotFound:
        raise ValueError(f"Network '{network_name}' not found.")

    except APIError as e:
        raise RuntimeError(f"Docker API error while deleting network '{network_name}': {e.explanation}")

    except Exception as e:
        raise RuntimeError(f"Unexpected error while deleting network '{network_name}': {e}")
