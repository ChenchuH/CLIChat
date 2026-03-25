import asyncio
import sys
import websockets
from rich.console import Console
from rich.text import Text
import os

console = Console()

WS_URL = "wss://clichat-test.onrender.com"
LOCAL_URL = "ws://localhost:10000"


async def main():
    url = LOCAL_URL  # switch to WS_URL when using Render

    async with websockets.connect(url) as ws:

        async def receiver():
            async for msg in ws:
                if msg.startswith("Client ") or msg.startswith("["):
                    if ":" in msg:
                        prefix, rest = msg.split(":", 1)

                        text = Text()
                        text.append(prefix, style="bold cyan")
                        text.append(":" + rest)

                        console.print(text)
                    else:
                        console.print(msg)
                else:
                    console.print(msg)

        async def sender():
            loop = asyncio.get_running_loop()
            while True:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                await ws.send(line.rstrip("\n"))

        await asyncio.gather(receiver(), sender())


if __name__ == "__main__":
    asyncio.run(main())