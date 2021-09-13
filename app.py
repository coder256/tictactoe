from flask import Flask, json, request, make_response
import math

app = Flask(__name__)


@app.route('/')
def index():
    # board = "xoxoxo x "
    board = request.args.get("board")
    if board is not None:
        print(f"board position 4:: {board[4]}")
        if isValidBoard(board) is False:
            return invalidBoard()

        # playable axes
        axes = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        wp = 0
        bp = 0
        for axis in axes:
            print(f"the axis:: {axis}")
            # check for playable space
            axis_string = f"{board[axis[0]]}{board[axis[1]]}{board[axis[2]]}"
            print(f"axis string ::{axis_string}::")
            if axis_string.count(" ") > 0:
                if isWinningPosition(axis_string):
                    print(f"winning position on:: {axis}")
                    wp += 1
                if isBlockablePosition(axis_string):
                    print(f"blockable position on:: {axis}")
                    bp += 1
            else:
                print("no playable space on this axis: ", axis)

        print(f"wp: {wp} --- bp: {bp}")

        return f"valid board :: {isValidBoard(board)}"
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
    if math.fabs(board.count("o") - board.count("x")) > 1:
        diff = math.fabs(board.count("o") - board.count("x"))
        print(f"illegal moves played :: {diff}")
        return False

    # make sure x has already won
    # playable axes
    axes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for axis in axes:
        # check for playable space
        axis_string = f"{board[axis[0]]}{board[axis[1]]}{board[axis[2]]}"
        if axis_string.count("x") == 3:
            print(f"x already won on {axis}")
            return False

    return True


def invalidBoard():
    return make_response("Invalid board"), 400


def isWinningPosition(axisString):
    if axisString.count("o") == 2:
        return True


def isBlockablePosition(axisString):
    if axisString.count("x") == 2:
        return True
