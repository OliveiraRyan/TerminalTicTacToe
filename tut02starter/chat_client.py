import sys
import socket
import select

_port = 5000
_max_msg_size = 256

def send_message(sock, msg):
    '''Send str msg to the socket sock. A socket.error is raised if the socket 
    cannot accept input.'''

    msg = bytes(msg, encoding="UTF-8")
    total_sent = 0
    while total_sent < len(msg):
        sent = sock.send(msg[total_sent: total_sent + _max_msg_size])
        total_sent += sent

if __name__ == "__main__":
    username = input("Who are you? ").strip()

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.connect(("localhost", _port))

    # TODO: complete this part.

    print("Connection terminated.")
    connection.close()
