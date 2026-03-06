import asyncio
import websockets
import os 

CL_ID = 1
CLIENTS_IDs = {}
CLIENTS = set() # passes the ws argument, its a list of clients stored as ws arugments for each

async def handler(ws):
    global CL_ID

    CLIENTS_IDs[ws] = CL_ID
    CL_ID += 1
    CLIENTS.add(ws)

    try:
        async for msg in ws:
            dead =[]
            for x in CLIENTS:
                if x is ws:
                    continue
                try:
                    sender_ID = CLIENTS_IDs[ws]
                    await x.send(f"Client {sender_ID}: {msg}")
                except Exception:
                    dead.append(x)
            for d in dead:
                CLIENTS.discard(d)
                CLIENTS_IDs.pop(d,None)
    finally:
        CLIENTS.discard(ws)
        CLIENTS_IDs.pop(ws, None)

async def main():
    port = int(os.environ.get("PORT", "10000")) # ties port the the enviorment variable thats the port, 10000 is a fallback ID if no port is given.
    host = "0.0.0.0"

    async with websockets.serve(handler, host, port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())