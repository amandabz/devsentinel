import docker
from docker.errors import NotFound


class MetricsCollector:
    def __init__(self):
        self.client = docker.from_env()

    def get_logs(self, container_name: str, tail: int = 50) -> str:
        try:
            container = self.client.containers.get(container_name)
            logs = container.logs(tail=tail).decode("utf-8")
            return logs
        except NotFound:
            return f"Container '{container_name}' not found."

    def get_recent_errors(self, container_name: str, tail: int = 50) -> list[str]:
        logs = self.get_logs(container_name, tail=tail)
        error_lines = [
            line for line in logs.splitlines()
            if any(word in line.lower() for word in ["error", "exception", "critical", "fatal"])
        ]
        return error_lines
