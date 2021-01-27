# Rush Hour Project
### Team Lightning Mcqueen: Tünde de Vries, Jeroen van der Borgh & Hanne Brouwer

## Case description
Rush hour is a puzzlegame in which the objective is to move the red car to the exit of the board.
However, on the board are several vehicles blocking the path of the red car to the exit.
These vehicles can be cars, that cover 2 spaces on the board, or trucks, that cover 3.

<img src="docs/Rushhour6x6_1.jpg" alt="Example of a Rush Hour board" width="200px">

In this case 7 different gameboards were given.
These 7 boards differ in size: the first 3 boards are 6x6, board 4 to 6 are 9x9, and board 7 is 12x12.
The boards also vary in difficulty to solve and statespace (how many boardstates are possible: the possible moves per turn ^ the number of moves made).

The objective in this case is to create an algorithm that is able to find the solution on each board with the smallest possible number of moves.
The difficulty of implementing an algorithm on the boards varies per board, as the statespace and difficulty is different for each board.