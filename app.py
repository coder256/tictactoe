from flask import Flask, json, request, make_response
import math
import urllib.parse

app = Flask(__name__)


@app.route('/')
def index():
    # board = "xoxoxo x "
    board = request.args.get("board")
    result = board
    if board is not None:
        if isValidBoard(board) is False:
            return invalidBoard()

        # playable axes
        axes = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        edge_axes = [
            [0, 1, 2], [0, 3, 6], [6, 7, 8], [2, 5, 8]
        ]
        diagonal_axes = [
            [0, 4, 8], [2, 4, 6]
        ]
        corners = [0, 2, 6, 8]

        # check if board is empty
        if board.count(" ") == 9:
            # return play(board, 0) todo uncomment line
            return f"valid board :: {urllib.parse.quote_plus(play(board, 0))}"  # todo comment out line

        # check if x played corner move first, play center
        if board.count("x") == 1 and board.count(" ") == 8 and board.index("x") in corners:
            print("x played corner first, play center")
            # play center
            # return play(board, 4) todo uncomment line
            return f"valid board :: {urllib.parse.quote_plus(play(board, 4))}"  # todo comment out line

        # check if x played non corner move first, play corner
        if board.count("x") == 1 and board.count(" ") == 8 and board.index("x") not in corners:
            print("x played non corner first, play corner")
            # play corner
            # return play(board, 8) todo uncomment line
            return f"valid board :: {urllib.parse.quote_plus(play(board, 8))}"  # todo comment out line

        wp = 0
        bp = 0
        pc = 0
        wAxis = []
        bAxis = []
        cAxis = []
        for axis in axes:
            print(f"the axis:: {axis}")
            # check for playable space
            axis_string = f"{board[axis[0]]}{board[axis[1]]}{board[axis[2]]}"
            print(f"axis string ::{axis_string}::")
            if axis_string.count(" ") > 0:
                if isWinningPosition(axis_string):
                    print(f"winning position on:: {axis}")
                    wAxis = axis
                    wp += 1
                if isBlockablePosition(axis_string):
                    print(f"blockable position on:: {axis}")
                    bAxis = axis
                    bp += 1
                if axis in edge_axes and isPlayableCorner(axis_string):
                    print(f"found playable corner on:: {axis}")
                    cAxis = axis
                    pc += 1

            else:
                print("no playable space on this axis: ", axis)

        print(f"wp: {wp} --- bp: {bp}")
        print(f"wAxis: {wAxis} --- bAxis: {bAxis} --- cAxis: {cAxis}")

        # play
        # play winning position
        if wp > 0:
            for position in wAxis:
                if board[position] == " ":
                    print("playable winning position ::", position)
                    result = play(board, position)
                    break
        elif bp > 0:
            # play blocking move
            for position in bAxis:
                if board[position] == " ":
                    print("playable blockable position ::", position)
                    result = play(board, position)
                    break
        elif isXForkPossible(board):
            print("x fork possible")
            # play along edge
            for edge in edge_axes:
                if board[edge[1]] == " ":
                    # return play(board, edge[1]) todo uncomment line
                    return f"valid board :: {urllib.parse.quote_plus(play(board, edge[1]))}" # todo comment line out
        elif pc > 0:
            # play corner
            if board[cAxis[0]] == " ":
                print(f"playable corner position :: {cAxis[0]}")
                # return play(board, cAxis[0]) todo uncomment line
                return f"valid board :: {urllib.parse.quote_plus(play(board, cAxis[0]))}"  # todo comment line out
            else:
                print(f"playable corner position :: {cAxis[2]}")
                # return play(board, cAxis[2]) todo uncomment line
                return f"valid board :: {urllib.parse.quote_plus(play(board, cAxis[2]))}"  # todo comment line out
        elif isOForkPossible(board):
            print(f"O fork possible")
            for axis in diagonal_axes:
                if board[axis[0]] == "o":
                    # return play(board, axis[2]) todo uncomment line
                    return f"valid board :: {urllib.parse.quote_plus(play(board, axis[2]))}"  # todo comment line out
                else:
                    # return play(board, axis[0]) todo uncomment line
                    return f"valid board :: {urllib.parse.quote_plus(play(board, axis[0]))}"  # todo comment line out
            pass
        else:
            print("NO PLANNED PLAYABLE POSITION FOUND, PLAY RANDOM")
            for i, c in enumerate(board):
                if c == " ":
                    return play(board, i)

        return f"valid board :: {urllib.parse.quote_plus(result)}"
        # return f"valid board :: {result}" todo uncomment line, comment above line
    else:
        return invalidBoard()


def isValidBoard(board):
    # validate length
    if len(board) != 9:
        print("Failed length test")
        return False

    # validate each character in board
    allowed_chacters = ['x', 'o', ' ']
    for c in board:
        if c not in allowed_chacters:
            print(f"invalid char:: {c}")
            return False

    # make sure o can play next
    diff = board.count("o") - board.count("x")
    if diff != 0 and diff != -1:
        # diff = math.fabs(board.count("o") - board.count("x"))
        print(f"illegal moves played :: {diff}")
        return False

    # make sure game hasn't already been won
    # playable axes
    axes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for axis in axes:
        # check for playable space
        axis_string = f"{board[axis[0]]}{board[axis[1]]}{board[axis[2]]}"
        if axis_string.count("x") == 3 or axis_string.count("o") == 3:
            print(f"already won on {axis}")
            return False

    return True


def invalidBoard():
    return make_response("Invalid board"), 400


def isWinningPosition(axisString):
    if axisString.count("o") == 2:
        return True

    return False


def isBlockablePosition(axisString):
    if axisString.count("x") == 2:
        return True

    return False


def isPlayableCorner(axisString):
    if axisString.count("x") == 1 and axisString.count(" ") == 2:
        return True

    return False

def isXForkPossible(board):
    diagonalOne = f"{board[0]}{board[4]}{board[8]}"
    diagonalTwo = f"{board[2]}{board[4]}{board[6]}"
    if diagonalOne.count("x") == 2 or diagonalTwo.count("x") == 2:
        return True

    return False

def isOForkPossible(board):
    diagonalOne = f"{board[0]}{board[4]}{board[8]}"
    diagonalTwo = f"{board[2]}{board[4]}{board[6]}"
    if (diagonalOne.count("o") == 1 and diagonalOne.count(" ") == 2) or (diagonalTwo.count("o") == 1 and diagonalTwo.count(" ") == 2):
        return True
    return False


def play(board, position):
    return board[:position] + "o" + board[position+1:]