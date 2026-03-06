import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed



WS_URL = "localhost"
PORT = 8765

async def handler(ws):
    name = await ws.recv() #waiting to recv from a client
    print(f"<<< {name}")

    welcomemsg= f"Hello {name}!"

    await ws.send(welcomemsg) #sends to a client
    print(f">>> {welcomemsg}")


async def main():
    async with serve(handler, WS_URL, PORT) as server:
        await server.serve_forever()

if __name__=="__main__":
    print("Websocket server started on ws://localhost:8765")
    asyncio.run(main())