import asyncio
import websockets

CLIENTS = set() # passes the ws argument, its a list of clients stored as ws arugments for each

async def handler(ws):
    CLIENTS.add(ws)
    try:
        async for msg in ws:
            dead =[]
            for x in CLIENTS:
                if x is ws:
                    continue
                try:
                    await x.send(msg)
                except Exception:
                    dead.append(x)
            for d in dead:
                CLIENTS.discard(d)
    finally:
        CLIENTS.discard(ws)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())