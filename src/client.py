import asyncio
import sys
import websockets
from rich.console import Console
from rich.text import Text

console = Console()

async def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "ws://localhost:8765"

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