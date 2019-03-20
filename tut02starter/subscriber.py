import socket

_port = 5000
_max_msg_size = 4096

if __name__ == "__main__":

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.connect(("localhost", _port))

    while True:
        msg = connection.recv(_max_msg_size).decode("UTF-8")
        if len(msg) == 0:
            break
        print("FROM BROADCASTER: {}".format(msg))

    connection.close()
    print("Connection terminated by server.")

