#  TIC TAC TOE SERVER

A server that plays tic tac toe or Noughts and Crosses build with python (using flask).  
1. Follows the strategy highlighted on [Wikipedia] (https://en.wikipedia.org/wiki/Tic-tac-toe)
2. Server plays O; order doesn't matter so it can play first or second.
3. Board is passed as a url encoded sting in this format (xo++++++o) where the '+' is for empty squares.  
Example call is http://localhost:5000/?board=xo++++++o
4. Returns the board in the same format with 'o' played if possible.
5. Server plays to win if possible and should be able to avoid defeat.

[![Tic tac toe baord](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Tic_tac_toe.svg/200px-Tic_tac_toe.svg.png)]
