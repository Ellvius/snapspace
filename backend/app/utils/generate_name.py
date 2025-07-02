import coolname
import uuid

def generate_container_name() -> str:
    words = coolname.generate()[:2]  # get first 2 words
    name = '-'.join(words)
    return name

def generate_unique_suffix() -> str:
    return uuid.uuid4().hex[:12]  # take first 12 hex chars
    
def generate_network_name() -> str:
    return uuid.uuid4().hex[:8]