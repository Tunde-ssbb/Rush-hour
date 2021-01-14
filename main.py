from code.classes.board import Board
from code.classes.car import Car
from code.classes.board import make_animation, save_log
from code.algorithms.random import Random_algorithm
from code.algorithms.depth_first_first_jeroen import depth_first_algorithm, check_solution, depth_first_main, remove_useless_moves
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
        random = Random_algorithm(game)
        random.run()
        print(f"Number of moves: {len(random.game.moves)}")


    # --------------------------- depth algorithm --------------------------
    elif algorithm == "depth_first":
        number_of_attempts = int(input("Number of attempts: "))
        max_moves = int(input("Maximum number of moves: "))
        solutions = depth_first_main(number_of_attempts, max_moves, size, data, True)

        if  len(solutions) > 0:
            short_solutions = []
            solution_number = 1
            for solution in solutions:
                short_solution = solution
                old_length = len(short_solution)
                new_length = old_length - 1
                while old_length > new_length:
                    #print(f"solution_number {solution_number} : length {len(short_solution)}")
                    old_length = len(short_solution)
                    short_solution = remove_useless_moves(short_solution, size, data)
                    new_length = len(short_solution)
                    #print(f"solution_number {solution_number} : to length {len(short_solution)}")
                
                #make_animation(short_solution, size, data, str(solution_number))
                #save_log(short_solution, str(solution_number))
                solution_number += 1
                print(f"solution_number {solution_number} length : {len(short_solution)}")
                short_solutions.append(short_solution)     
        #print(short_solutions[0])
        #print(sys.getrecursionlimit())


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
        sys.exit(0)

    # print(lengths)
    # lengths = [5,7,3,9,13,12,12,9,7,7]
    # lengths = np.array(lengths)
    # range_lengths = range(np.min(lengths), np.max(lengths)) 
    # height = np.zeros(len(range_lengths))

    # for i in range(len(range_lengths)):
    #     height[i] = np.count_nonzero(lengths == range_lengths[i])

    # print(range_lengths, height)
    # plt.plot(np.array(range_lengths),height)
    # fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    # ax.bar(np.array(range_lengths), height)
    # fig.show()