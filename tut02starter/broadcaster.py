import sys
import socket
import select

_port = 5000
_timeout = 600
_max_msg_size = 256

def setup_server(port):
    '''Return a server socket bound to the specified port.'''

    print("Starting on Hostname: localhost on Port: ", port)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.setblocking(0)
    connection.bind(('localhost', port))
    connection.listen(5)
    return connection

def send_messages(sockets, msg):
    '''Send bytes msg to each socket in the dict sockets. If a socket has died,
    remove it from sockets.'''

    to_remove = []
    msg = b"Breaking news: " + msg
    for sock in sockets:
        total_sent = 0
        try:
            while total_sent < len(msg):
                sent = sock.send(msg[total_sent: total_sent + _max_msg_size])
                total_sent += sent
        except socket.error:
            print("Client", sockets[sock], "disconnected.")
            to_remove.append(sock)

    for sock in to_remove:
        del sockets[sock]

if __name__ == "__main__":

    connection = setup_server(_port)
    inputs = [connection, sys.stdin]
    clients = dict()
    while True:
        inps, outs, errors = select.select(inputs, [], [], _timeout)
        if inps == []: # Timed out
            break
        for inp in inps:
            if inp == sys.stdin: # Terminal input
                print("Broadcasting...")
                send_messages(clients, sys.stdin.readline().rstrip().encode("UTF-8"))
            elif inp == connection: # New connection
                (client, address) = connection.accept()
                clients[client] = address
                print("Accepted new client", address)
    print("Terminating")
    connection.close()

