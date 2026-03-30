import asyncio
import websockets
import os
import aiosqlite
from datetime import datetime

CL_ID = 1
CLIENTS_IDs = {}
CLIENTS = set()  # passes the ws argument, its a list of clients stored as ws arugments for each

DB_FILE = "chat.db"


async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_message(client_id, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT INTO messages (client_id, message, timestamp) VALUES (?, ?, ?)",
            (client_id, message, timestamp)
        )
        await db.commit()
    return timestamp


async def send_history(ws, limit=20):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("""
            SELECT client_id, message, timestamp
            FROM messages
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        await cursor.close()

    rows.reverse()

    if rows:
        await ws.send("---- Recent Messages ----")
        for client_id, message, timestamp in rows:
            await ws.send(f"Client {client_id}: {message}")
        await ws.send("-------------------------")


async def handler(ws):
    global CL_ID

    CLIENTS_IDs[ws] = CL_ID
    CL_ID += 1
    CLIENTS.add(ws)

    await ws.send(f"__ID__:{CLIENTS_IDs[ws]}")  # ← send ID first
    await send_history(ws)

    try:
        async for msg in ws:
            msg = msg.strip()
            if not msg:
                continue

            sender_ID = CLIENTS_IDs[ws]
            await save_message(sender_ID, msg)

            dead = []
            others = [x for x in CLIENTS if x is not ws]
            tasks = []

            for x in others:
                tasks.append(x.send(f"Client {sender_ID}: {msg}"))

            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for client, result in zip(others, results):
                    if isinstance(result, Exception):
                        dead.append(client)

            for d in dead:
                CLIENTS.discard(d)
                CLIENTS_IDs.pop(d, None)

    finally:
        CLIENTS.discard(ws)
        CLIENTS_IDs.pop(ws, None)


async def main():
    await init_db()

    port = int(os.environ.get("PORT", "10000"))  # ties port the the enviorment variable thats the port, 10000 is a fallback ID if no port is given.
    host = "0.0.0.0"

    async with websockets.serve(handler, host, port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())