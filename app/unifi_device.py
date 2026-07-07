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
            self._connect = await asyncssh.connect(
                self.ip,
                username=settings.username,
                password=settings.password,
                known_hosts=None,
            )

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

        start = time.time()
        u1 = UnifiDevice("192.168.15.65")
        task1 = await u1.run_command("uname -a")
        print(task1)
        stop1 = time.time() - start
        print(f"Время подключения к точке и выполнения 1 команды, {stop1}")
        start2 = time.time()
        task2 = await u1.run_command("mca-dump")
        print(task2)
        stop2 = time.time() - start2
        print(f"Время выполнения 2 команды, {stop2}")


asyncio.run(main())
