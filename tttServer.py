#!/usr/bin/env python3

import argparse
import socket
import os
import random
import time

_max_msg_size = 256

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, help='The port to listen on')
# parser.add_argument('--verbose', help='Should display the game turn by turn', action='store_true')
args = parser.parse_args()

sock = socket.socket()
host = socket.gethostname()
sock.bind((host, args.port))

sock.listen(2)

print(host)

print('Waiting for client 1...')
conn1, addr1 = sock.accept()


print('Waiting for client 2...')
conn2, addr2 = sock.accept()

turn = 0
winner = None

p1Turn = random.randint(0,1)
p2Turn = not p1Turn

#implement logic for distributing player 1 and player 2 turns
#send the entire moves array back and forth (easiest to deal with and not that much data)
#print messages on the player's consoles
#determine win condition here - valid moves can be done but its better client side since they resume their turn
#everything else should be client I guess

def send_message(sock, msg):
    '''Send bytes msg to each socket in the dict sockets and return a list of sockets
    which have died.'''

    msg = bytes(msg, encoding="UTF-8")
    to_remove = []
    total_sent = 0
    try:
        while total_sent < len(msg):
            sent = sock.send(msg[total_sent: total_sent + _max_msg_size])
            total_sent += sent
    except socket.error:
        print("Error occured, message not sent")
        return
    #     to_remove.append(sock)
    # return to_remove

print('Game starting...')
while turn < 9 and winner == None:
    turn += 1

    #send message (game state) to BOTH players

    if (p1Turn):
        #wait for p1 move
        continue
    elif (p2Turn):
        #wait for p2 move
        continue

    #swap turns
    p1Turn = not p1Turn
    p2Turn = not p2Turn

