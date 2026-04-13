import docker
from datetime import datetime, timezone


class DockerMonitor:
    def __init__(self):
        self.client = docker.from_env()

    def get_containers(self):
        return self.client.containers.list(all=True)

    def get_container_stats(self, container):
        name = container.name
        status = container.status

        if status != "running":
            return {
                "name": name,
                "status": status,
                "cpu_percent": 0.0,
                "mem_usage_mb": 0.0,
                "mem_percent": 0.0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        stats = container.stats(stream=False)

        # CPU
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                       stats["precpu_stats"]["system_cpu_usage"]
        num_cpus = stats["cpu_stats"]["online_cpus"]
        cpu_percent = (cpu_delta / system_delta) * num_cpus * 100

        # Memoria
        mem_usage = stats["memory_stats"]["usage"]
        mem_limit = stats["memory_stats"]["limit"]
        mem_percent = (mem_usage / mem_limit) * 100

        return {
            "name": name,
            "status": status,
            "cpu_percent": round(cpu_percent, 2),
            "mem_usage_mb": round(mem_usage / 1024 / 1024, 2),
            "mem_percent": round(mem_percent, 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_all_stats(self):
        containers = self.get_containers()
        return [self.get_container_stats(c) for c in containers]
