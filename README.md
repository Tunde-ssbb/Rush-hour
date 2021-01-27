# Rush Hour Project
##### Team Lightning Mcqueen: Tünde de Vries, Jeroen van der Borgh & Hanne Brouwer

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

#### Terminology
Short explanations on the terminology used in this readme and repository:
- Car = in this readme and repository used to signify vehicles (of length 2 and 3)
- Move = combination of car and number of steps
- Boardstate = places of cars on the board in a specific situation


## Usage
In the section below is described how to create various results from the code in the repository. 

### main&#46;py

All the code that was used to create results can be accessed and run trhough main&#46;py. The command line code to run the program is structured as follows:

<code>python main&#46;py [board number] [algorithm name] </code>

For <code>board number</code>, an integer between 1 and 7 is expected, indicating wich board you would like to be run. 
The field <code>algorithm name</code> expects one of the following inputs:

- <code>random</code>
- <code>optimalisation</code>
- <code>depth_first</code>
- <code>play</code>

#### random
If this option is chosen the user is asked for additional inputs:

- <code>Number of attempts</code> expects an integer number, indicating how many random solutions will be looked for (e.g. filling in 5 will return 5 solutions)
- <code>Maximum moves</code> expects and integer number, indicating what the bound is for random solutions. (e.g. filling in 100 will only return solutions of less than 100 moves)
- <code>Log solution</code> expects either <code>y</code>(es) or <code>n</code>(o), indicating whether the solutions will be logged. Entering <code>y</code> will create a csv file with the found solution under <code>data/logs/random_board[board number].csv</code>

If all information is filled correctly, the algorithm will be run.

#### optimalisation
If this option is chosen the user is asked for additional inputs:

- <code>Number of attempts</code> expects an integer number, indicating how many solutions will be looked for (e.g. filling in 5 will return 5 solutions)
- <code>Maximum moves</code> expects and integer number, indicating what the bound is for the random solutions. (a high number will improve the speed of the random part of the algorithm, and decrease that of the improvment algorithm)
- <code>Create animation</code> expects either <code>y</code>(es) or <code>n</code>(o), indicating whether the solutions will be logged. Entering <code>y</code> will create a gif file with the found solution animated under <code>data/results/[index of solution].gif</code>
- <code>Log solution</code> expects either <code>y</code>(es) or <code>n</code>(o), indicating whether the solutions will be logged. Entering <code>y</code> will create a csv file with the found solution under <code>data/logs/[index of solution].csv</code>

If all information is filled correctly, the algorithm will be run.

#### optimalisation
If this option is chosen the user is asked for additional inputs:

- <code>Number of attempts</code> expects an integer number, indicating how many solutions will be looked for (e.g. filling in 5 will return 5 solutions)
- <code>Maximum moves</code> expects and integer number, indicating what the bound is for the random solutions. (a high number will improve the speed of the random part of the algorithm, and decrease that of the improvment algorithm)
- <code>Create animation</code> expects either <code>y</code>(es) or <code>n</code>(o), indicating whether the solutions will be logged. Entering <code>y</code> will create a gif file with the found solution animated under <code>data/results/[index of solution].gif</code>
- <code>Log solution</code> expects either <code>y</code>(es) or <code>n</code>(o), indicating whether the solutions will be logged. Entering <code>y</code> will create a csv file with the found solution under <code>data/logs/[index of solution].csv</code>

If all information is filled correctly, the algorithm will be run.

#### depth_first
If this option is chosen the user is asked for additional inputs:

- <code>Maximum moves</code> expects and integer number, indicating what the bound is for the solutions. State space will be searched up to this depth
- <code>Dynamic bound</code> expects either <code>y</code>(es) or <code>n</code>(o). Entering <code>n</code> will limit the depth_first algorithm at a fixed depth (namely, at the maximum moves). Entering <code>y</code> will dynamically change the maximum search depth to the shortest solution that was found so far (thus decreasing the statespace).
- <code>Print all</code> expects either <code>y</code>(es) or <code>n</code>(o). Entering <code>y</code> will cause all found solutions to be printed in the terminal. 
- <code>Log solution</code> expects either <code>y</code>(es) or <code>n</code>(o), indicating whether the solutions will be logged. Entering <code>y</code> will create a csv file with the found solution under <code>data/logs/depth_first[board_number].csv</code>
- <code>Create animation</code> expects either <code>y</code>(es) or <code>n</code>(o), indicating whether the solutions will be logged. Entering <code>y</code> will create a gif file with the found solution animated under <code>data/results/depth_first[board_number].gif</code>
- <code>Filter</code> expects either <code>None</code> or <code>a list of solution movesets</code>. Entering <code>a list of solution movesets</code> will look at the solutions, and extract cars that do not move throughout any of the found solutions. Branches where these cars are moved are pruned in the algorithm to reduce running time. Entering <code>None</code> will not affect the algorithm.

If all information is filled correctly, the algorithm will be run. The best solution (if any solution exists) will be printed at the end.

#### play

This options allows the user to play the chosen gameboard directly in the terminal. If it is chosen, the user is repeatedly asked for a <code>Car</code>, for which a car id (e.g. "X") is needed, and for a step (e.g. -1) indicating the number of steps the car should take. (negative is up/left, positive is down/right)

