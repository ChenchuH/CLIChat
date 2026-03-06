import asyncio
import sys
import websockets
from rich.console import Console
from rich.text import Text
import os

console = Console()

WS_URL="wss://clichat-test.onrender.com"
LOCAL_URL = "wss://localhost:8765"
#switch url source based on where you are testing, WS_URL is the render.io dash

async def main():
    url = WS_URL #or LOCAL_URL

    async with websockets.connect(url) as ws:
        async def receiver():
            async for msg in ws:    
                # Expected format: "Client 1: hello"
                if msg.startswith("Client "):
                    prefix, rest = msg.split(":", 1)

                    text = Text()
                    text.append(prefix, style="bold cyan")
                    text.append(":" + rest)

                    console.print(text)
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