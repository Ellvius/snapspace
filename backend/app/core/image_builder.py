import os
import docker
import docker.errors
from app.core.docker_config import client

def build_all_templates(template_root: str = "templates"):
    built_images = []
    logs = []

    for dir_entry in os.scandir(template_root):
        if dir_entry.is_dir():
            dockerfile_path = os.path.join(dir_entry.path, "Dockerfile")
            if os.path.isfile(dockerfile_path):
                image_tag = f"{dir_entry.name}-env"
                logs.append(f"🔧 Building image: {image_tag}")

                try:
                    response = client.api.build(
                        path=dir_entry.path,
                        tag=image_tag,
                        rm=True,
                        decode=True
                    )

                    for chunk in response:
                        if 'stream' in chunk:
                            line = chunk['stream'].strip()
                            print(line)
                            logs.append(line)

                    logs.append(f"✅ {image_tag} image built successfully!\n")
                    print(f"✅ {image_tag} image built successfully!")
                    built_images.append(image_tag)

                except docker.errors.BuildError as e:
                    msg = f"❌ Failed to build {image_tag}: {e}"
                    print(msg)
                    logs.append(msg)
                except docker.errors.APIError as e:
                    msg = f"❌ Docker API error for {image_tag}: {e}"
                    print(msg)
                    logs.append(msg)
                except Exception as e:
                    msg = f"❌ Unexpected error for {image_tag}: {e}"
                    print(msg)
                    logs.append(msg)

    return {
        "built_images": built_images,
        "logs": logs
    }
