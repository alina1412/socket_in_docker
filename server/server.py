import json
import socket

import threading


HEADER_LENGTH = 64
PORT = 5050
SERVER_ADDR = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_ADDR, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
MESSAGE_BUF_LEN = 8

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def get_full_message(conn, msg_length):
    message_buf = ""
    while len(message_buf) < msg_length:
        msg = (conn.recv(MESSAGE_BUF_LEN)).decode("utf-8")
        print(msg)
        if not msg.strip():
            break
        message_buf += msg
    return message_buf.strip()


def get_msg_len_from_header(client_conn):
    msg_length = client_conn.recv(HEADER_LENGTH).decode("utf-8")
    if msg_length:
        msg_length = int(msg_length)
        return msg_length
    return 0


def prepare_answer(msg):
    data = json.loads(msg)
    password = data.get("password", "")
    if len(password) < 4:
        return json.dumps(
            {
                "acknowleged": False,
                "error": "the length of the password shall be >= 4",
            }
        )
    return json.dumps({"acknowleged": True})


def handle_client(client_conn, client_addr):
    try:
        connected = True
        while connected:
            msg_length = get_msg_len_from_header(client_conn)
            message = get_full_message(client_conn, msg_length)
            if not message or message == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{client_addr}] {message}")
            ans = prepare_answer(message)
            client_conn.send(ans.encode("utf-8"))
    except Exception as exc:
        print("error", exc)
    client_conn.close()


def start():
    server.listen(5)
    print(f"Server is listening on {SERVER_ADDR}")
    while True:
        client_conn, client_addr = server.accept()
        print(f"{client_addr} connected")
        # handle_client(client_conn, client_addr)
        thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("Server is starting...")
start()
