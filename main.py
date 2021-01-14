from code.classes.board import Board
from code.classes.car import Car
from code.classes.board import make_animation, save_log
from code.algorithms.random import Random_algorithm
from code.algorithms.depth_first import depth_first_algorithm, depth_first_main
from code.algorithms.improve_solution import improve_solutions
from code.algorithms.breadth_first_Tünde import breadth_first_algorithm
import random
import sys
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # dictionary of board numbers with corresponding sizes
    board_sizes = { "1": 6, "2": 6, "3": 6,
                    "4": 9, "5": 9, "6": 9,
                    "7": 12, "test" : 4}

    # check if command line argument input is valid
    if len(sys.argv) != 3:
        print("Invalid input. Use format: main.py <board number> <algorithm>")
        sys.exit(0)

    board_number = sys.argv[1]
    algorithm = sys.argv[2]

    # check if board number is valid
    if board_number not in board_sizes:
        print("Invalid board number. Choose a board number from 1 to 7")
        sys.exit(0)

    size = board_sizes[board_number]
    data = f"./data/gameboards/Rushhour{board_sizes[board_number]}x{board_sizes[board_number]}_{board_number}.csv"


    # --------------------------- Random algorithm --------------------------
    if algorithm == "random":
        # create board object and run algorithm
        game = Board(size, data)
        random = Random_algorithm(game, data)
        random.run()
        print(f"Number of moves: {len(random.game.moves)}")


    # --------------------------- depth algorithm --------------------------
    elif algorithm == "depth_first":
        number_of_attempts = int(input("Number of attempts: "))
        max_moves = int(input("Maximum number of moves: "))
        solutions = depth_first_main(number_of_attempts, max_moves, size, data, True)
        short_solutions = improve_solutions(solutions, size, data, animation=False, log=False)




    # --------------------------- breadth algorithm --------------------------
    elif algorithm == "breadth_first":
        game = Board(size, data)
        game.load_board()
        shortest, lengths = breadth_first_algorithm(game)
        make_animation(shortest, board_sizes[board_number], data)
        print(len(lengths)," solutions were found.")


    # ------------------------------------------------------------------------
    else:
        print("Invalid algorithm input. Choose: random, depth_first, or breadth_first")
<<<<<<< HEAD
        sys.exit(0)


=======
        sys.exit(0)
>>>>>>> ebc011c397d2605304644033eb5e66984496b47b
