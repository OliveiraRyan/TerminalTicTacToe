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
#determine win condition here - valid moves can be done but its better client side since they resume their turn upon illegal move instantly
#everything else should be client I believe

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
        print("Error occurred, message not sent")
        return

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

def blankRow():
    for col in range(17):
        if (col%6==5):
            print('|', end='')
        else:
            print(' ', end='')
    print()

def inputRow(row):
    counter = 0
    for col in range(17):
        if (col%6==2):
            print(moves[row][counter], end='')
            counter += 1
        elif (col%6==5):
            print('|', end='')
        else:
            print(' ', end='')
    print()

def lineRow():
    for col in range(17):
        if (col%6==5):
            print('|', end='')
        else:
            print('_', end='')
    print()

def drawBoard():
    '''Format the gamestate into a pretty TicTacToe board! The helper functions
    above have simple tasks, which are explained above their respective 
    function call in this function.'''

    #'clear' has been removed so server app retains move history
    # os.system('clear')
    for row in range(9):
        if (row%3 == 0 or row == 8):
            #print blanks for row
            blankRow()
        elif (row%3 == 1):
            #the user has input on this row
            inputRow(row//3)
        elif (row%3 == 2):
            #draw horizontal line
            lineRow()
    print()

#TODO Add play again function
# def playAgain(winner):
    # send_message(conn1, 'Player 1 has won!')
    # send_message(conn2, winner)

    # return


print('\nGame starting...', flush=True)

 
#send initial message telling the clients who goes first
send_message(conn1, str(p1Turn))
send_message(conn2, str(p2Turn))
time.sleep(1)
send_message(conn1, '1')
send_message(conn2, '2')
time.sleep(1)

#start the game!
while turn < 9 and winner == None:
    turn += 1



    #send message (game state) to BOTH players
    if (p1Turn):
        playerTurn = 1
        print("Player 1's turn...", flush=True)
        #wait for p1 move
        send_message(conn1, "Your move!")
        send_message(conn2, "Waiting for opponent...")

        # moves = conn1.recv(_max_msg_size).decode("UTF-8")
        moves = pickle.loads(conn1.recv(_max_msg_size))

        send_moves(conn2, moves)
        
    elif (p2Turn):
        playerTurn = 2
        print("Player 2's turn...", flush=True)
        #wait for p2 move
        send_message(conn1, "Waiting for opponent...")
        send_message(conn2, "Your move!")

        # moves = conn2.recv(_max_msg_size).decode("UTF-8")
        moves = pickle.loads(conn2.recv(_max_msg_size))

        send_moves(conn1, moves)

    #Print gamestate
    drawBoard()
    # print(moves, flush=True)
    
    #swap turns
    p1Turn = not p1Turn
    p2Turn = not p2Turn
    
    #check if game has been won, and ask players if they would like to play again
    if (winCondition()):
        time.sleep(2)
        winner = 'Player %d has won!' % playerTurn
        print(winner, flush=True)
        
        #server should currently terminate at this point -- can do reset game feature later
        # playAgain(winner)

        break

    

