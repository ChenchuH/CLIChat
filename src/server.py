import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed



WS_URL = "localhost"
PORT = 8765

async def handler(ws):
    print("Client Connected")
    try:
        async for msg in ws:
            msg = await ws.recv()
            print(f"Message received: {msg}")
            await ws.send(f"echo: {msg}")
    except ConnectionClosed as e:
        print(f"Client disconnected with {e.code}: {e.reason}")


async def main():
    async with serve(handler, WS_URL, PORT):
        await asyncio.Future()

if __name__=="__main__":
    print("Websocket server started on ws://localhost:8765")
    asyncio.run(main())