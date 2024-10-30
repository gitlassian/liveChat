from flask import Flask, render_template, request, redirect, url_for
from flask_sock import Sock
import random
import json

app = Flask(__name__)
sock = Sock(app)

colors = ["red", "yellow", "orange", "green", "lightblue", "blue", "purple"]

clients_colors = {}

clients = {}

@app.route("/login", methods=["POST", "GET"])
def login():
    if (request.method == "GET"):
        if(request.cookies.get('nick')):
            return redirect(url_for("chat"))
        else:
            return render_template("login.html")
    if (request.method == "POST"):
        try:
            if request.get_json().get("nick") not in clients.keys():
                clients[request.get_json().get("nick")]=""
                return {"redirect": True}
            else:
                return {"redirect": False}
        except:
            return {"data": "restricted"}
        
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/chat", methods=["GET"])
def chat():
    if (request.method == "GET"):
        if(request.cookies.get('nick')):
            return render_template("chat.html")
        else:
            return redirect(url_for("login"))
        
@sock.route("/")
def socket(websocket):
    while True:
        message = websocket.receive()

        if websocket not in list(clients.values()):
            clients[message]=websocket
            clients_colors[message]=colors[random.randint(0,6)]
            print("Added new client: " + message)
            websocket.send(json.dumps(["added", "black", str(message)]))
        else:
            print("Recieved new message: "+ message)
            if(len(message)>1):
                for client in list(clients.values()):
                    client.send(json.dumps([message,clients_colors[list(clients.keys())[list(clients.values()).index(websocket)]],list(clients.keys())[list(clients.values()).index(websocket)]]))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80,
        debug=True
    )

# async def main(websocket: websockets.WebSocketClientProtocol, path: str):
#     print("Added new client!")
#     while True:
#         message = await websocket.recv()
#         print("Recieved new message: "+ message)
        
#         for client in clients.values:
#             try:
#                 await client.send(message)
#             except:
#                 pass

# run_websocket = websockets.serve(main, "localhost", 8765)

# async def run_flask():
#     app.run(
#         host="localhost",
#         port=80
#     )

# asyncio.get_event_loop().run_until_complete(start_server)
# print("Chat server started on ws://localhost:8765")
#     asyncio.get_event_loop().run_forever()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.gather(
#     run_flask(),

# ))
# loop.run_forever()
