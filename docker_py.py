import docker
from dataclasses import dataclass


@dataclass
class container_data:
    id: str
    image: str
    cmd: str
    created: str
    status: str
    ports: str
    name: str
    cpu_usage: str
    memory_usage: str


class docker_py:
    def __init__(self):
        self.client = docker.from_env()

    def docker_ps_stats(self):
        container_list = self.client.containers.list(all=True)
        container_list_data = []
        for container in container_list:
            cmd = container.attrs["Config"]["Cmd"]
            if isinstance(cmd, list):
                cmd = " ".join(cmd)

            created = container.attrs["Created"]

            ports = container.attrs["NetworkSettings"]["Ports"]
            if ports:
                ports = str(ports)
            else:
                ports = "N/A"

            if container.image.tags:
                image = container.image.tags[0]
            else:
                image = "N/A"

            stats = container.stats(stream=False)
            if container.status == "running":
                stats = container.stats(stream=False)
                cpu_stats = stats["cpu_stats"]
                cpu_usage = cpu_stats["cpu_usage"]["total_usage"]
                memory_stats = stats["memory_stats"]
                mem_stats_stats = memory_stats["stats"]
                memory_usage = ((memory_stats["usage"] - mem_stats_stats["cache"]) / memory_stats["limit"]) * 100
            else:
                cpu_usage = 0.0
                memory_usage = 0.0

            container_data_instance = container_data(id=container.id[:12], image=image, cmd=cmd, created=created, status=container.status, ports=ports, name=container.name, cpu_usage=cpu_usage, memory_usage=memory_usage)

            container_list_data.append(container_data_instance)
        return container_list_data

    def docker_create(self, name, img):
        try:
            self.client.containers.create(img, name=name)
            create_status = "success"
        except Exception as e:
            print(e)
            create_status = "failed"
        return create_status

    def docker_stop(self, name):
        try:
            container = self.client.containers.get(name)
            container.stop()
            stop_status = "success"
        except Exception as e:
            print(e)
            stop_status = "failed"
        return stop_status

    def docker_start(self, name):
        try:
            container = self.client.containers.get(name)
            container.start()
            start_status = "success"
        except Exception as e:
            print(e)
            start_status = "failed"
        return start_status

    def docker_remove(self, name):
        try:
            container = self.client.containers.get(name)
            container.stop()
            container.remove()
            remove_status = "success"
        except Exception as e:
            print(e)
            remove_status = "failed"
        return remove_status
