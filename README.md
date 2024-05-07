
# Game notation

### Board Notation
* A quoridor board is 9x9 squares, with options to place walls in between any 4 valid squares
* With this constraint, a wall cannot be placed on the perimeter or fractionally overlapping a given square
* The board columns will be a-i and rows 1 - 9, with the left-most square proximal to player 1 being a1

###  Wall placement
* Every wall must touch four squares.
* A wall move is denoted by the closest square to a1, with a horizontal h or vertical v orientation.
* ex.) Player 1's first move is to block player 2 between rows 8 and 9, 
then notation would be: d8v OR e8v because to block the forward pawn move, 
I can place in one of two positions overlapping e8.

### Pawn placement
* A pawn move will be denoted by the square to which it moves
* ex.) If player 1's first move forward one square, they will have moved b5

### Position Notation
* The least of information needed to describe a position using Forsyth Edwards Notation is:
  * Horizontal wall positions
    * single string (eg. e2b2 if two horizontal walls were placed on row 2)
  * Vertical wall positions
    * string string (eg. c4c6 if two vertical walls were stacked on column c)
  * Occupied squares by both player's pawns
    * player 1 (eg. e1 at the beginning of the game)
    * player 2 (eg. e9 at the beginning of the game)
  * Remaining walls at each player's disposal
    * player 1 (eg. 10 at the beginning of the game)
    * player 2 (eg. 10 at the beginning of the game)
* So, notation is generally described as [1]/[2]/[3]/[4]
  * Eg, at the beginning of the game: //e1e9/(10)10

First two moves, for example:
1. //e1e9/(10)10 -> //e2e9/(10)10
2. //e2e9/(10)10 -> 