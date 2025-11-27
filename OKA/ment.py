import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 55555

class DruidClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.positions = {}

        self.root = tk.Tk()
        self.root.title("Друїдський зв’язок")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e2e')

        title = tk.Label(self.root, text="Зв’язок з духами землі", font=("Segoe UI", 16, "bold"),
                         bg='#1e1e2e', fg='#cdd6f4')
        title.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='#94e2d5')
        self.canvas.pack(pady=10)

        self.chat = scrolledtext.ScrolledText(self.root, height=8, state='disabled',
                                              bg='#1e1e2e', fg='#cdd6f4')
        self.chat.pack(fill='both', expand=True, padx=20, pady=5)

        input_frame = tk.Frame(self.root, bg='#1e1e2e')
        input_frame.pack(fill='x', padx=20, pady=5)

        self.entry = tk.Entry(input_frame, font=("Segoe UI", 12))
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind("<Return>", self.send_message)

        send_btn = tk.Button(input_frame, text="→", command=self.send_message,
                             bg='#89b4fa', fg='white', width=5)
        send_btn.pack(side='right')

        self.connect()

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
            self.name = tk.simpledialog.askstring("Ім'я", "Вкажи своє ім'я духа:")
            if not self.name:
                self.name = "анонімний_дух"
            self.sock.send(self.name.encode('utf-8'))

            threading.Thread(target=self.listen_server, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося підключитися:\n{e}")
            self.root.quit()

    def listen_server(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    break
                msg = json.loads(data)

                if msg["type"] == "join":
                    self.log_chat(f"→ {msg['user']} увійшов у коло")
                elif msg["type"] == "leave":
                    self.log_chat(f"← {msg['user']} покинув коло")
                elif msg["type"] == "message":
                    self.log_chat(f"{msg['user']}: {msg['text']}")
                elif msg["type"] == "position":
                    self.update_position(msg["user"], msg["x"], msg["y"])
                elif msg["type"] == "all_positions":
                    for user, (x, y) in msg["positions"].items():
                        if x is not None:
                            self.update_position(user, x, y, force=True)

            except:
                break

    def log_chat(self, text):
        self.chat.config(state='normal')
        self.chat.insert('end', text + "\n")
        self.chat.config(state='disabled')
        self.chat.see('end')

    def update_position(self, user, x, y, force=False):
        self.positions[user] = (x, y)
        self.redraw_map()

    def redraw_map(self):
        self.canvas.delete("all")
        w, h = 600, 400
        offset_x, offset_y = 100, 50

        for i in range(0, w, 50):
            self.canvas.create_line(i, 0, i, h, fill="#74c7ec", dash=(2,2))
        for i in range(0, h, 50):
            self.canvas.create_line(0, i, w, i, fill="#74c7ec", dash=(2,2))

        for user, (x, y) in self.positions.items():
            if x is None or y is None:
                continue
            px = offset_x + x * 10
            py = offset_y + y * 10

            color = '#f38ba8' if user == self.name else '#a6e3a1'
            self.canvas.create_oval(px-10, py-10, px+10, py+10, fill=color, outline='white')
            self.canvas.create_text(px, py-20, text=user, fill='white', font=("Segoe UI", 10, "bold"))

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, 'end')

        if text.startswith("/move "):
            try:
                _, x, y = text.split()
                msg = json.dumps({
                    "type": "position",
                    "user": self.name,
                    "x": float(x),
                    "y": float(y)
                })
                self.sock.send(msg.encode('utf-8'))
            except:
                self.log_chat("Неправильна команда. Використовуй: /move 52.1 24.5")
        else:
            msg = json.dumps({
                "type": "message",
                "user": self.name,
                "text": text
            })
            self.sock.send(msg.encode('utf-8'))
            self.log_chat(f"Я: {text}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    import tkinter.simpledialog
    app = DruidClient()
    app.run()