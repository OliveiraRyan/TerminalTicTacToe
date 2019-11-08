import os

player = '1'
moves = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
playerLetter = {
    '1': 'X',
    '2': 'O'
}
swapPlayer = {
    '1': '2',
    '2': '1'
}


def blankRow():
    for col in range(17):
        if (col % 6 == 5):
            print('|', end='')
        else:
            print(' ', end='')
    print()


def inputRow(row):
    counter = 0
    for col in range(17):
        if (col % 6 == 2):
            print(moves[row][counter], end='')
            counter += 1
        elif (col % 6 == 5):
            print('|', end='')
        else:
            print(' ', end='')
    print()


def lineRow():
    for col in range(17):
        if (col % 6 == 5):
            print('|', end='')
        else:
            print('_', end='')
    print()


def drawBoard():
    os.system('clear')
    for row in range(9):
        if (row % 3 == 0 or row == 8):
            # print blanks for row
            blankRow()
        elif (row % 3 == 1):
            # the user has input on this row
            inputRow(row//3)
        elif (row % 3 == 2):
            # draw horizontal line
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
            drawBoard()
    playerMove()


def validMove(inputValue):
    try:
        return inputValue < 3 and inputValue >= 0
    except:
        return False


def winCondition():
    for letter in ['X', 'O']:
        for i in range(3):
            # check rows for win
            if (moves[i][0] == moves[i][1] == moves[i][2] == letter):
                return True
            # check cols for win
            elif (moves[0][i] == moves[1][i] == moves[2][i] == letter):
                return True
        # check diagonals for win
        if (moves[0][0] == moves[1][1] == moves[2][2] == letter):
            return True
        elif (moves[0][2] == moves[1][1] == moves[2][0] == letter):
            return True
    return False


def play():
    global moves, player
    moveCounter = 0

    while moveCounter < 9:
        moveCounter += 1
        playerTurn()
        if (winCondition()):
            print('Player %s has won!' % player)
            break
        player = swapPlayer[player]

    if (moveCounter == 9):
        print('It\'s a tie!')
    print('Play Again?')
    if (input("Press '1' for YES and any other key to EXIT!\n") == '1'):
        moves = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        drawBoard()
        play()
    else:
        print("Goodbye!")


def start():
    drawBoard()
    print('Welcome To Terminal Tic-Tac-Toe')
    print('Player 1 will play as X')
    print('Player 2 will play as O')
    if (input("Press '1' to play and any other key to EXIT!\n") != '1'):
        print("Goodbye!")
        exit()
    play()


start()
