import docker
import pprint
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


class docker_py:
    def __init__(self):
        self.client = docker.from_env()

    def docker_ps(self):
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

            container_data_instance = container_data(
                id=container.id[:12],
                image=image,
                cmd=cmd,
                created=created,
                status=container.status,
                ports=ports,
                name=container.name,
            )

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

    def docker_stats(self):
        try:
            for i in self.client.containers.list():
                pprint.pprint(i.stats(stream=False))
        except Exception as e:
            print(e)
