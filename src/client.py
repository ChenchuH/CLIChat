import asyncio
import sys
import websockets
from rich.console import Console
from rich.text import Text
import os
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML

console = Console()

WS_URL = "wss://clichat-test.onrender.com"
LOCAL_URL = "ws://localhost:10000"

# switch url source based on where you are testing, WS_URL is the render.io dash

#getting id
async def receive_id(ws):
    msg = await ws.recv()
    if msg.startswith("__ID__:"):
        return int(msg.split(":")[1])
    raise ValueError(f"Expected ID message, got: {msg}")

async def main():
    url = LOCAL_URL  # or WS_URL
    session = PromptSession()
    # my_id = None

    async with websockets.connect(url) as ws:

        my_id = await receive_id(ws) 
        print(f"Connected as Client {my_id}")

        async def receiver():
            async for msg in ws:
                if msg.startswith("Connecting as Client "):
                    my_id = msg[len("Connecting as Client"):]
                    print_formatted_text(HTML(f'<gray>Connected as Client {my_id}</gray>'))
                elif msg.startswith("Client "):
                    prefix, rest = msg.split(":", 1)
                    print_formatted_text(HTML(f'<red>{prefix}</red>:{rest}'))
                else:
                    print_formatted_text(HTML(msg))

        async def sender():
            with patch_stdout():
                while True:
                    try:
                        prompt_str = HTML(f'<cyan>Client {my_id or "?"} &gt;</cyan> ')
                        line = await session.prompt_async(prompt_str)
                    except (EOFError, KeyboardInterrupt):
                        break
                    if line.strip():
                        await ws.send(line)
 

        await asyncio.gather(receiver(), sender())

if __name__ == "__main__":
    asyncio.run(main())