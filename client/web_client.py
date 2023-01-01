import socket


HEADER = 64
PORT = 5050
SERVER = "server-cont"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send_to_server(msg):
    message = msg.encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receive_from_server():
    answer = client.recv(1024).decode("utf-8")
    # print(answer)
    return answer


if __name__ == "__main__":
    send_to_server("Hello World!")
    send_to_server(DISCONNECT_MESSAGE)
