import os
import sys
import socket
import select
import pickle
import time

_port = 5001
_max_msg_size = 256

player = '1'
moves = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
playerLetter = {
    '1': 'X',
    '2': 'O'
}
swapPlayer = {
    '1': '2',
    '2': '1'
}

def send_message(sock, msg):
    '''Send str msg to the socket sock. A socket.error is raised if the socket 
    cannot accept input.'''

    # msg = bytes(msg, encoding="UTF-8")
    msg = pickle.dumps(msg)
    # total_sent = 0
    # while total_sent < len(msg):
    #     sent = sock.send(msg[total_sent: total_sent + _max_msg_size])
    #     total_sent += sent
    sock.sendall(msg)

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
    os.system('clear')
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


def playerTurn():
    global player
    print("Player %s\'s Turn:\n" % player)

    def playerMove():
        try:
            row, col = int(input('Row :'))-1, int(input('Column :'))-1
        except:
            print('Invalid Input! Please Try Again!')
            playerMove()
            return
        
        if (not validMove(row) or not validMove(col) or moves[row][col] != ' '):
            print('Invalid Input! Please Try Again!')
            playerMove()
            return

        else:
            moves[row][col] = playerLetter[player]
            #drawBoard()
    playerMove()

def validMove(inputValue):
    try:
        return inputValue < 3 and inputValue >= 0
    except:
        return False
        
def play():
    global moves, player
    moveCounter = 0 #for use later, when implementing reset feature

    #most of this is done in server

    # while moveCounter < 9:
    #     moveCounter += 1
    #     playerTurn()
    #     if (winCondition()):
    #         print('Player %s has won!' % player)
    #         break
    #     player = swapPlayer[player]
        

    # if (moveCounter == 9):
    #     print('It\'s a tie!')
    # print('Play Again?')
    # if (input("Press '1' for YES and any other key to EXIT!")=='1'):
    #     moves = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    #     drawBoard()
    #     play()

    #can change True to < 9 later -- when implementing restart game feature
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.connect(("DESKTOP-V2I4740", _port))

    while True:
        
        msg = connection.recv(_max_msg_size).decode("UTF-8")
        if len(msg) == 0:
            break
        print("FROM SERVER: {}".format(msg))
        if (msg == "Your move!"):
            drawBoard()
            playerTurn()
            send_message(connection, moves)
            print("send moves")
        elif (msg == "Waiting for opponent..."):
            moves = pickle.loads(connection.recv(_max_msg_size))

        

    print("Connection terminated.")
    connection.close()

def start():
	drawBoard()
	print('Welcome To Terminal Tic-Tac-Toe')
	print('Player 1 will play as X')
	print('Player 2 will play as O')
	if input("Press '1' to play and any other key to exit!\n") != '1':
		exit()
	play()


start()

