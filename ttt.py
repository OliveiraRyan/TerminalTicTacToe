import os

player = 1
moves = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]

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
    


def player1():
    pass

def player2():
    pass

def validMove(inputValue):
    return (inputValue > 2 or inputValue < 0)

def winCondition():
    for letter in ['X', 'O']:
        for i in range(3):
            #check rows for win
            if (moves[i][0] == moves[i][1] == moves[i][2] == letter):
                return letter
            #check cols for win
            elif (moves[0][i] == moves[1][i] == moves[2][i] == letter):
                return letter
        #check diagonals for win
        if (moves[0][0] == moves[1][1] == moves[2][2] == letter):
            return letter
        elif (moves[0][2] == moves[1][1] == moves[2][0] == letter):
            return letter
        


def play():
    pass

def start():
	drawBoard()
	print('Welcome To Terminal Tic-Tac-Toe')
	print('Player 1 will play as X')
	print('Player 2 will play as O')
	if input("Press '1' to play and any other key to exit!\n") != '1':
		exit()
	play()


start()

