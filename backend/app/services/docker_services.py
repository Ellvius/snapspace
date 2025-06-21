import docker.errors
from app.core.docker_config import client
import docker

def run_container(image: str):
    try:
        container = client.containers.run(
            image=image,
            detach=True,
            tty=True
        )
        return {
            "status": "success",
            "container": {
                "id": container.id,
                "short_id": container.short_id,
                "name": container.name
            }
        }
    except docker.errors.ImageNotFound:
        return {
            "status": "error",
            "message": f"Image '{image}' not found"
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": str(e)
        }
        

def list_containers(all: bool = True):
    try:
        containers = client.containers.list(all=all)
        return [
            {
                "id": c.id,
                "short_id": c.short_id,
                "name": c.name,
                "image": c.image.tags,
                "status": c.status
            }
            for c in containers
        ]
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": str(e)
        }


def stop_container(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {
            "status": "success",
            "message": f"Container stopped, id: {container_id}"
        }
    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"Container with ID '{container_id}' not found"
        }
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": str(e)
        }