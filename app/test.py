import asyncssh
import asyncio

HOST = "192.168.15.65"
USER = "admin"
PASSWORD = "r0vgh0vfn"
COMMAND = "uname -a"


async def main():
    async with asyncssh.connect(
        HOST,
        username=USER,
        password=PASSWORD,
        known_hosts=None,
    ) as conn:
        result = await conn.run(COMMAND)
        print("STDOUT - читает")
        print(result.stdout)
        print("STRERR")
        print(result.stderr)
        print("EXIT", result.exit_status)


asyncio.run(main())
