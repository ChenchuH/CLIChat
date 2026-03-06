from websockets.sync.client import connect


def hello():
    WS_URL = "ws://localhost:8765"

    with connect(WS_URL) as ws:
        ClientName=input("Enter your name: ")

        ws.send(ClientName) #sends to server
        print(f">>> {ClientName}")

        greeting = ws.recv() #waiting to recive from server
        print(f"<<< {greeting}")


if __name__=="__main__":
    hello()
