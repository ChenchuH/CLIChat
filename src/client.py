# import asyncio
# import sys
# import websockets
# from rich.console import Console
# from rich.text import Text
# import os

# console = Console()

# WS_URL="wss://clichat-test.onrender.com"
# LOCAL_URL = "ws://localhost:8765"
# #switch url source based on where you are testing, WS_URL is the render.io dash

# async def main():
#     url = LOCAL_URL #or LOCAL_URL

#     async with websockets.connect(url) as ws:
#         client_id = None
#         async def receiver():
#             nonlocal client_id    

#             async for msg in ws:
#                 #announce the id on connection
#                 if msg.startswith("Connecting as Client "):
#                     my_id = msg[len("Connecting as Client")]
#                     ##console.print(f"[dim]Confirmed connection as Client {client_id}[/dim]")

#                 # Expected format: "Client 1: hello"
#                 if msg.startswith("Client "):
#                     prefix, rest = msg.split(":", 1)

#                     text = Text()
#                     text.append(prefix, style="bold cyan")
#                     text.append(":" + rest)

#                     console.print(text)
#                 else:
#                     console.print(msg)

#         async def sender():
#             loop = asyncio.get_running_loop()
#             while True:
#                 line = await loop.run_in_executor(None, sys.stdin.readline)
#                 if not line:
#                     break
                
#                 #format messgae for the user
#                 line = line.rstrip("/n")

#                 ##text with the extra output
#                 ##-------------
#                 # text = Text()
#                 # text.append(f"Client {client_id}", style="bold green")
#                 # text.append(f": {line}")
#                 # console.print(text)
#                 # await ws.send(line.rstrip("\n"))
#                 ##-------------

#                 ##text without extra output. might have visual bugs when sending at same time. need to test if looks off in differnent clis bc ANSI works different for some of the,
#                 # sys.stdout.write("\033[1A\033[2K")
#                 # sys.stdout.flush()
#                 # text = Text()
#                 # text.append(f"Client {client_id}", style="bold green")
#                 # text.append(f": {line}")
#                 # console.print(text)
#                 # await ws.send(line)

#         await asyncio.gather(receiver(), sender())

# if __name__ == "__main__":
#     asyncio.run(main())


# import asyncio
# import websockets
# from prompt_toolkit import PromptSession
# from prompt_toolkit.patch_stdout import patch_stdout
# from prompt_toolkit.formatted_text import HTML

# WS_URL = "wss://clichat-test.onrender.com"
# LOCAL_URL = "ws://localhost:8765"

# async def main():
#     url = LOCAL_URL
#     session = PromptSession()
#     my_id = None

#     async with websockets.connect(url) as ws:

#         async def receiver():
#             nonlocal my_id
#             async for msg in ws:
#                 if msg.startswith("Connecting as Client "):
#                     my_id = msg[len("Connecting as Client"):]
#                     print(f"Connected as Client {my_id}\n")
#                 elif msg.startswith("Client "):
#                     prefix, rest = msg.split(":", 1)
#                     # patch_stdout ensures this prints above the input bar
#                     print(f"\033[96m{prefix}\033[0m:{rest}")
#                     #print('happi')
#                 else:
#                     print(msg)

#         async def sender():
#             with patch_stdout():
#                 while True:
#                     try:
#                         prompt_str = HTML(f'<ansigreen>Client {my_id or "?"} &gt;</ansigreen> ')
#                         line = await session.prompt_async(prompt_str)
#                     except (EOFError, KeyboardInterrupt):
#                         break
#                     if line.strip():
#                         await ws.send(line)
#                         # Echo own message above the input bar
#                         print(f"\033[92mClient {my_id}\033[0m: {line}")

#         await asyncio.gather(receiver(), sender())

# if __name__ == "__main__":
#     asyncio.run(main())


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
                    print_formatted_text(HTML(f'<cyan>{prefix}</cyan>:{rest}'))
                else:
                    print_formatted_text(HTML(msg))
 
        async def sender():
            with patch_stdout():
                while True:
                    try:
                        prompt_str = HTML(f'<green>Client {my_id or "?"} &gt;</green> ')
                        line = await session.prompt_async(prompt_str)
                    except (EOFError, KeyboardInterrupt):
                        break
                    if line.strip():
                        await ws.send(line)
                        print_formatted_text(HTML(f'<green>Client {my_id}</green>: {line}'))
 
        await asyncio.gather(receiver(), sender())
 
if __name__ == "__main__":
    asyncio.run(main())


# typing on top
# #promptoolkit button bar (cool)
# something wrong w formatting v3. but it double text