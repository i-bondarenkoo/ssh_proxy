from app.unifi_device import UnifiDevice
import asyncio
import time


class SSHManager:

    def __init__(self):
        self.devices: dict = {}

    async def run(self, ip: str, command: str):
        if ip not in self.devices:
            self.devices[ip] = UnifiDevice(ip)
        result = await self.devices[ip].run_command(command)
        return result


if __name__ == "__main__":

    async def main():
        manager = SSHManager()
        list_tasks = []
        start = time.time()
        task1 = asyncio.create_task(manager.run("192.168.15.2", "uname -a"))
        list_tasks.append(task1)
        asyncio.sleep(250)
        task2 = asyncio.create_task(manager.run("192.168.15.2", "info"))
        list_tasks.append(task2)
        # task2 = asyncio.create_task(manager.run("192.168.15.65", "uname -a"))
        # list_tasks.append(task2)
        # task3 = asyncio.create_task(manager.run("192.168.15.1", "uname -a"))
        # list_tasks.append(task3)
        # task4 = asyncio.create_task(manager.run("192.168.15.2", "uname -a"))
        # list_tasks.append(task4)
        # task5 = asyncio.create_task(manager.run("192.168.15.2", "info"))
        # list_tasks.append(task5)
        # task6 = asyncio.create_task(manager.run("192.168.15.155", "uname -a"))
        # list_tasks.append(task6)
        # task7 = asyncio.create_task(manager.run("192.168.15.65", "jopa"))
        # list_tasks.append(task7)
        result = await asyncio.gather(*list_tasks)
        print(result)
        print(
            f"Время выполнения 2 запросов ={time.time() - start} вместе с делеем 250 сек"
        )

    asyncio.run(main())
