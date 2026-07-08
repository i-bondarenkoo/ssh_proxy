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
        task2 = asyncio.create_task(manager.run("192.168.15.65", "uname -a"))
        list_tasks.append(task2)
        task3 = asyncio.create_task(manager.run("192.168.15.1", "uname -a"))
        list_tasks.append(task3)
        task4 = asyncio.create_task(manager.run("192.168.15.2", "uname -a"))
        list_tasks.append(task4)
        result = await asyncio.gather(*list_tasks)
        print(result)
        print(f"Время выполнения 4 запросов ={time.time() - start}")

    asyncio.run(main())
