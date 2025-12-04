import socket
import threading
import json
from datetime import datetime

HOST = '127.0.0.1'  
PORT = 55555

clients = {}
positions = {}        
lock = threading.Lock()

def broadcast(message, exclude=None):
    """Розсилає JSON всім, крім exclude"""
    dead_clients = []
    for client in clients:
        if client != exclude:
            try:
                client.send(message.encode('utf-8'))
            except:
                dead_clients.append(client)

    for dead in dead_clients:
        disconnect_client(dead)

def disconnect_client(client_sock):
    with lock:
        if client_sock in clients:
            name = clients[client_sock]["name"]
            del clients[client_sock]
            if name in positions:
                del positions[name]
            print(f"Дух {name} покинув коло.")
            broadcast(json.dumps({
                "type": "leave",
                "user": name,
                "time": datetime.now().strftime("%H:%M")
            }))

def handle_client(client_sock, addr):
    try:
        # отримуємо ім'я
        client_sock.send("Вкажи своє ім'я духа: ".encode('utf-8'))
        name = client_sock.recv(1024).decode('utf-8').strip()
        if not name:
            name = f"дух_{addr[1]}"

        with lock:
            clients[client_sock] = {"name": name, "addr": addr}
            positions[name] = None

        print(f"{name} увійшов у коло з {addr}")

        broadcast(json.dumps({
            "type": "join",
            "user": name,
            "time": datetime.now().strftime("%H:%M")
        }))

        client_sock.send(json.dumps({
            "type": "all_positions",
            "positions": positions
        }).encode('utf-8'))

        while True:
            data = client_sock.recv(1024).decode('utf-8')
            if not data:
                break

            try:
                msg = json.loads(data)

                if msg["type"] == "position":
                    x, y = float(msg["x"]), float(msg["y"])
                    with lock:
                        positions[name] = (x, y)
                    broadcast(json.dumps({
                        "type": "position",
                        "user": name,
                        "x": x,
                        "y": y
                    }), client_sock)

                elif msg["type"] == "message":
                    broadcast(json.dumps({
                        "type": "message",
                        "user": name,
                        "text": msg["text"],
                        "time": datetime.now().strftime("%H:%M")
                    }), client_sock)

            except json.JSONDecodeError:
                pass
            except Exception as e:
                print(f"Помилка обробки: {e}")
                break

    except:
        pass
    finally:
        disconnect_client(client_sock)
        client_sock.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Сервер друїдів слухає {HOST}:{PORT}...")

    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()

