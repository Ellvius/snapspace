import docker
import docker.errors
from app.core.docker_config import client


# Create a container in an isolated network
def create_container(image_name: str, network_name: str, subdomain: str, internal_port: int = 8080):
    try:
        # Create isolated network
        # client.networks.create(network_name, driver="bridge")
        
        container = client.containers.run(
            image=image_name,
            detach=True,
            ports={},  
            tty=True,
            network=network_name,
            labels={
                "traefik.enable": "true",
                f"traefik.http.routers.{subdomain}.rule": f"Host(`{subdomain}.localhost`)",
                f"traefik.http.services.{subdomain}.loadbalancer.server.port": str(internal_port),
                "traefik.docker.network": network_name
            }
        )
        return {
            "status": "success",
            "container": {
                "id": container.id,
                "short_id": container.short_id,
                "name": container.name,
                "image": image_name,
                "container_network": network_name,
            },
            "url": f"http://{subdomain}.localhost"
        }
    except docker.errors.ImageNotFound:
        return {
            "status": "error",
            "message": f"Image '{image_name}' not found"
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Docker API error while creating container: {str(e)}"
        }
        

# List all containers (default: all)
def list_containers(all: bool = True):
    try:
        containers = client.containers.list(all=all)
        return {
            "status": "success",
            "containers": [
                {
                    "id": c.id,
                    "short_id": c.short_id,
                    "name": c.name,
                    "image": c.image.tags[0],
                    "status": c.status,
                }
                for c in containers
            ]
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Failed to list containers: {str(e)}"
        }


# Stop a running container by ID
def stop_container(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {
            "status": "success",
            "message": f"Container '{container.name}' stopped successfully"
        }
    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"No container found with ID '{container_id}'"
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Failed to stop container: {str(e)}"
        }
        
        
# Remove a container by ID (stops first if running)
def remove_container(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.remove(force=True)
        return {
            "status": "success",
            "message": f"Container '{container.name}' removed successfully."
        }
    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"No container found with ID '{container_id}'."
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Failed to remove container: {str(e)}"
        }


# Restart a container by ID
def restart_container(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.restart()
        return {
            "status": "success",
            "message": f"Container '{container.name}' restarted successfully."
        }
    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"No container found with ID '{container_id}'."
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Failed to restart container: {str(e)}"
        }


# Get logs from a container by ID
def get_container_logs(container_id: str, tail: int = 100):
    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=tail).decode("utf-8")
        return {
            "status": "success",
            "message": f"Fetched logs from container '{container.name}'.",
            "logs": logs
        }
    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"No container found with ID '{container_id}'."
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Failed to fetch logs: {str(e)}"
        }