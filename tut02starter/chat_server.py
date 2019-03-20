import sys
import socket
import select

_port = 5000
_max_msg_size = 256

def setup_server(port):
    '''Return a server socket bound to the specified port.'''

    print("Starting on Hostname:", socket.gethostname(), "on Port: ", port)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.setblocking(0)
    connection.bind((socket.gethostname(), port))
    connection.listen(5)
    return connection

def send_messages(sockets, msg):
    '''Send bytes msg to each socket in the dict sockets and return a list of sockets
    which have died.'''

    msg = bytes(msg, encoding="UTF-8")
    to_remove = []
    for sock in sockets:
        total_sent = 0
        try:
            while total_sent < len(msg):
                sent = sock.send(msg[total_sent: total_sent + _max_msg_size])
                total_sent += sent
        except socket.error:
            to_remove.append(sock)
    return to_remove

def handle_message(sock, sockets):
    '''Process the message sent on socket sock and then return a list of client 
    sockets that have been terminated.'''

    to_remove = []
    msg = sock.recv(_max_msg_size).decode("UTF-8")
    if len(msg.strip()) == 0:
        return [sock]

    firstfield = msg.strip().split()[0]
    if firstfield.startswith("<") or len(firstfield) == 0 or \
       (sockets[sock][1] == None and firstfield != "/user"):
        to_remove.append(sock)

    elif firstfield.startswith("/"):
        remainder = msg.strip()[len(firstfield):].strip()
        if firstfield == "/user" and sockets[sock][1] == None:
            if len(remainder) > 0:
                sockets[sock] = (sockets[sock][0], remainder)
                to_remove = send_messages(sockets, "%s has connected." % remainder)
            else:
                to_remove.append(sock)
        elif firstfield == "/users":
            to_remove = send_messages([sock], "%d users are online." % (len(sockets)))
        elif firstfield == "/bye":
            to_remove = send_messages([sock], "Simonsays ...")
            to_remove += send_messages(sockets, "%s has left the room." % sockets[sock][1])
            to_remove.append(sock)
        else:
            to_remove = send_messages([sock], "Server says: Nice try!")

    else:
        to_remove = send_messages(sockets, "%s says: %s" % (sockets[sock][1], msg.strip()))

    return to_remove

if __name__ == "__main__":
    connection = setup_server(_port)

    inputs = [connection, sys.stdin]
    clients = {}
    while 1:
        inps, outs, errors = select.select(inputs, [], [])

        for inp in inps:
            if inp == sys.stdin: # Terminal input
                send_messages(clients, "<SERVER MESSAGE> " + sys.stdin.readline().rstrip())
            elif inp == connection: # New connection
                (client, address) = connection.accept()
                clients[client] = (address, None)
                inputs.append(client)
                print("Accepted new client", address)
            else:
                try:
                    to_remove = handle_message(inp, clients)
                except socket.error:
                    to_remove = [inp]
                for client in to_remove:
                    print("Dropping client", clients[client])
                    try:
                        send_messages([client], "/bye")
                    except socket.error:
                        pass
                    del clients[client]
                    inputs.remove(client) 
                    client.close()

    print("Terminating")
    connection.close()
