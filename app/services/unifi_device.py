import asyncssh
import time
from app.core.config import settings
import asyncio
from app.core.logging import logger
from app.services.dependencies import timer


class UnifiDevice:
    def __init__(self, ip: str):
        self.ip = ip
        self._lock = asyncio.Lock()
        self._connect = None

    async def _get_ssh_session(self):
        if self._connect is None or self._connect.is_closed():
            logger.info(f"Устанавливаем SSH соединение с - {self.ip}")
            self._connect = await asyncssh.connect(
                self.ip,
                username=settings.username,
                password=settings.password,
                known_hosts=None,
                # время для подключения к точке по ssh
                connect_timeout=1,
                # каждые 30 сек отправлять пинги на точку, для проверки соединения
                keepalive_interval=30,
            )
        else:
            logger.info("Соединение уже установлено, переиспользуем")

    @timer
    async def run_command(self, command: str):
        async with self._lock:
            for _ in range(2):
                try:
                    await self._get_ssh_session()
                    result = await self._connect.run(command)
                    return {
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "exit_status": result.exit_status,
                    }
                    # print(result.stdout)
                    # print(result.stderr)
                    # print(result.exit_status)
                except asyncssh.Error:
                    logger.warning(
                        "Проблема с установлением SSH соединения, попыток - 1"
                    )
                    self._connect = None
                    continue
                except OSError:
                    logger.warning("Incorrect ip_address has been entered")
                    return {
                        "error": f"Failed call connect, ip_address - {self.ip}, port - 22"
                    }
            logger.error("Неудалось установить ssh-соединение, количество попыток - 2")
            return {
                "error": f"Неудалось установить ssh-соединение, количество попыток - 2"
            }

    async def close(self):
        if self._connect is not None and not self._connect.is_closed():
            self._connect.close()
            await self._connect.wait_closed()
            logger.info("Приложение  закрывается, закрываем активные SSH подключения")


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
