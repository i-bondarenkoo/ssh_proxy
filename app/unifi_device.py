import asyncssh
import time
from app.core.config import settings
import asyncio


class UnifiDevice:
    def __init__(self, ip: str):
        self.ip = ip
        self._lock = asyncio.Lock()
        self._connect = None

    async def _get_ssh_session(self):
        if self._connect is None:
            print(f"Я создаю новое подключение, по адресу {self.ip}")
            self._connect = await asyncssh.connect(
                self.ip,
                username=settings.username,
                password=settings.password,
                known_hosts=None,
            )
        else:
            print("Подключение уже есть, я возьму его")

    async def run_command(self, command: str):
        async with self._lock:
            await self._get_ssh_session()
            result = await self._connect.run(command)
            return result.stdout
            # print(result.stdout)
            # print(result.stderr)
            # print(result.exit_status)


if __name__ == "__main__":

    async def main():
        list_tasks = []
        u1 = UnifiDevice("192.168.15.2")
        u2 = UnifiDevice("192.168.15.65")
        start = time.time()
        task1 = asyncio.create_task(u1.run_command("uname -a"))
        list_tasks.append(task1)
        task2 = asyncio.create_task(u2.run_command("uname -a"))
        list_tasks.append(task2)
        result = await asyncio.gather(*list_tasks)
        stop = time.time() - start
        print(result)
        print(
            f"Время выполнения 2 команд для разных точек, при конкурентности ={stop} "
        )
        u3 = UnifiDevice("192.168.15.1")
        st2 = time.time()
        task3 = u3.run_command("uname -a")
        result = await task3
        stop2 = time.time() - st2
        print(result)
        print(f"Время выполнения команды ={stop2}")
        task4 = u2.run_command("uname -a")
        s3 = time.time()
        await task4
        st4 = time.time() - s3
        print(f"Время выполнения команды с готовым ssh соединением ={st4}")
        s5 = time.time()
        res = await asyncio.gather(
            u2.run_command("uname -a"),
            u2.run_command("uname -a"),
        )
        print(
            f"Две команды к 1 точке, через gather, время выполнения ={time.time() -s5}"
        )

    asyncio.run(main())
