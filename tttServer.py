#!/usr/bin/env python3

import argparse
import socket
import os
import random
import pickle
import time

_max_msg_size = 256

moves = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, help='The port to listen on')
args = parser.parse_args()

sock = socket.socket()
host = socket.gethostname()
sock.bind(('', args.port))

sock.listen(2)

print("Port: %d" % args.port)
print("Host: %s" % host)

print('Waiting for client 1...', flush=True)
conn1, addr1 = sock.accept()

print('Waiting for client 2...', flush=True)
conn2, addr2 = sock.accept()

turn = 0
winner = None

#value is True when it is the player's turn
p1Turn =  0 == random.randint(0,1)
p2Turn = not p1Turn

#implement logic for distributing player 1 and player 2 turns
#send the entire moves array back and forth (easiest to deal with and not that much data)
#print messages on the player's consoles
#determine win condition here - valid moves can be done but its better client side since they resume their turn
#everything else should be client I guess

def send_message(sock, msg):
    '''Send bytes msg to each socket in the dict sockets and return a list of sockets
    which have died.'''

    global conn1, conn2
    # print(msg)
    msg = bytes(msg, encoding="UTF-8")
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

def send_moves(sock, msg):
    '''Send str msg to the socket sock. A socket.error is raised if the socket 
    cannot accept input.'''

    msg = pickle.dumps(msg)
    sock.sendall(msg)

def winCondition():
    for letter in ['X', 'O']:
        for i in range(3):
            #check rows for win
            if (moves[i][0] == moves[i][1] == moves[i][2] == letter):
                return True
            #check cols for win
            elif (moves[0][i] == moves[1][i] == moves[2][i] == letter):
                return True
        #check diagonals for win
        if (moves[0][0] == moves[1][1] == moves[2][2] == letter):
            return True
        elif (moves[0][2] == moves[1][1] == moves[2][0] == letter):
            return True
    return False


print('\nGame starting...', flush=True)

 
#send initial message telling the clients who goes first
send_message(conn1, str(p1Turn))
send_message(conn2, str(p2Turn))
time.sleep(1)
send_message(conn1, '1')
send_message(conn2, '2')
time.sleep(1)
while turn < 9 and winner == None:
    turn += 1

    #send message (game state) to BOTH players

    print(p1Turn, flush=True)
    print(p2Turn, flush=True)

    if (p1Turn):
        playerTurn = 1
        # print("we in bois", flush=True)
        #wait for p1 move
        send_message(conn1, "Your move!")
        send_message(conn2, "Waiting for opponent...")

        # moves = conn1.recv(_max_msg_size).decode("UTF-8")
        moves = pickle.loads(conn1.recv(_max_msg_size))

        send_moves(conn2, moves)
        
    elif (p2Turn):
        playerTurn = 2
        # print("we in bois 2", flush=True)
        #wait for p2 move
        send_message(conn1, "Waiting for opponent...")
        send_message(conn2, "Your move!")

        # moves = conn2.recv(_max_msg_size).decode("UTF-8")
        moves = pickle.loads(conn2.recv(_max_msg_size))

        send_moves(conn1, moves)

    print(moves, flush=True)
    
    
    if (winCondition()):
        winner = 'Player %d has won!' % playerTurn
        # send_message(conn1, winner)
        # send_message(conn2, winner)
        print(winner, flush=True)
        #server should terminate at this point -- can do reset game feature later
        break

    #swap turns
    p1Turn = not p1Turn
    p2Turn = not p2Turn

