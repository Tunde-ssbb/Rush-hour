from code.classes.board import Board
from code.classes.car import Car
from code.util import make_animation, save_log, get_cars
from code.algorithms.random import Random_algorithm
<<<<<<< HEAD
from code.algorithms.depth_first_smart_archive import depth_first_main
=======
from code.algorithms.depth_first_smart_archive import depth_first_algorithm, depth_first_main
>>>>>>> 74f960ee1cc2b891e43474c857cb04ae38595c65
from code.algorithms.improve_solution import improve_solutions
from code.algorithms.breadth_first import breadth_first_algorithm
from code.heuristics.winning_comparison import winning_comparison
from code.heuristics.a_star import a_star_heuristic
from code.heuristics.test_heuristic import test_heuristic
import random
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import time



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
        number_of_attempts = int(input("Number of attempts: "))  
        max_moves = int(input("Maximum number of moves: ")) 
        random = Random_algorithm(size, data)
        solutions = random.run(number_of_attempts, max_moves)
        print(random.length_best_solution)
        print("starting optimalization")
        short_solutions = improve_solutions(solutions, size, data, animation=True, log=False)

    # --------------------------- depth algorithm --------------------------
    elif algorithm == "depth_first":
        number_of_attempts = int(input("Number of attempts: "))
        max_moves = int(input("Maximum number of moves: "))
        
        start = time.time()
        solutions = depth_first_main(number_of_attempts, max_moves, size, data, fixed_solutions=False)
        end = time.time()
        for solution in solutions:
            save_log(solution, str(board_number))
            print(f"solution of length {len(solution)} found.")
        print(f"time to find a solution: {round(end - start,2)} seconds")   


    # --------------------------- breadth algorithm --------------------------
    elif algorithm == "breadth_first":
        game = Board(size, data)
        game.load_board()
        shortest, lengths = breadth_first_algorithm(game)
        make_animation(shortest, board_sizes[board_number], data)
        print(len(lengths)," solutions were found.")


    # ------------------------------------------------------------------------
    elif algorithm == "test_improve_solution":
        """
        board 7:
        lengths = [25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 49, 50, 51, 53, 54, 55, 58, 69, 72]
        heigths = [44, 43, 26, 30, 26, 16, 6, 1, 1, 2, 3, 5, 4, 1, 2, 3, 4, 3, 5, 3, 6, 4, 4, 2, 1, 1, 1, 1, 1, 1]
        """

        number_of_attempts = 250
        max_moves = 6000
        random = Random_algorithm(size, data)

        start = time.time()
    
        start = begin = time.time()
        solutions = random.run(number_of_attempts, max_moves)
        end = time.time()
        print(f"time to find solutions: {round(end - start,2)} seconds")

        start = time.time()
        short_solutions = improve_solutions(solutions, size, data, animation=False, log=False)
        end = time.time()
        print(f"time to optimize solution: {round(end - start,2)} seconds")
        print(f"Total time: {round(end - begin,2)} seconds")

        
        results = []
        for solution in short_solutions:
            results.append(len(solution))
        
        lengths = []
        for result in results:
            if result not in lengths:
                lengths.append(result)

        lengths.sort()
        heights = [0]* len(lengths)
        for i in range(len(lengths)):
            for result in results:
                if result == lengths[i]:
                    heights[i] += 1
        
        print()

        print(f"shortest solution = {lengths[0]} with {round((heights[0]/sum(heights))* 100, 2)} %")

        ax = plt.figure(1).gca()

        #ax = fig.add_subplot(111)
        ax.bar(lengths,heights)
        print(lengths)
        print(heights)
        ax.set_xlabel(f"number_of_moves")
        ax.text(0.45, 0.93, f"shortest solution = {lengths[0]} with {round((heights[0]/sum(heights))* 100, 2)} %", verticalalignment='center', transform=ax.transAxes, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 5})
        ax.set_title(f" {number_of_attempts} solutions of board {board_number}")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        #plt.xticks(lengths)
        plt.savefig(f'{number_of_attempts}solutions_of_board{board_number}-2.png')
     
    elif algorithm == "test_heuristic":
        game = Board(size, data)
        #heuristic = "blocking_cars"
        #heuristic = "winning_comparison"
        heuristic = "a_star"
        scores = test_heuristic(game, heuristic, size, data, best=False)
        
        for score in scores:
            print(score)

        game = Board(size, data)
        scores = test_heuristic(game, heuristic, size, data, best=True)
        
        for score in scores:
            print(score)

    # ------------------------------------------------------------------------        
    elif algorithm == "check":
        # random = Random_algorithm(size, data)
        # random.run(1)
        # winning_hash = random.get_winning_hash()
        
        board = Board(size, data)
        board.load_board()
        board.draw_board()

        while True:
            move = input("Car:")
            if move == "q":
                break
            step = int(input("Step: "))
            if move not in board.cars.keys():
                print("Invalid car")
            elif board.validate_move(move, step):
                board.move(move, step)
                board.log_move(move, step)
                board.draw_board()
                
                score = a_star_heuristic(board)
                print(score)

                if board.won():
                    print("Game was won")
                    break
            else:
                print("Invalid move")

        make_animation(board.moves, board_sizes[board_number], data, "test")
        #board.save_log()
        print("Game ended")

    # ------------------------------------------------------------------------
    else:
        print("Invalid algorithm input. Choose: random, depth_first, or breadth_first")
        sys.exit(0)
