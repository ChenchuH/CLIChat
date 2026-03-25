import asyncio
import websockets
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML
 
WS_URL = "wss://clichat-test.onrender.com"
LOCAL_URL = "ws://localhost:8765"
 
async def main():
    url = LOCAL_URL
    session = PromptSession()
    my_id = None
 
    async with websockets.connect(url) as ws:
 
        async def receiver():
            nonlocal my_id
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
                        print_formatted_text(HTML(f'<cyan>Client {my_id}</cyan>: {line}'))
 
        await asyncio.gather(receiver(), sender())
 
if __name__ == "__main__":
    asyncio.run(main())

