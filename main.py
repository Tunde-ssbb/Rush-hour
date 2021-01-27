from code.classes.board import Board
from code.classes.car import Car
from code.util import make_animation, save_log, get_cars, bar_plot_of_solutions
from code.algorithms.random import random_main
from code.algorithms.depth_first_smart_archive import depth_first_smart_archive_main
from code.algorithms.improve_solution import improve_solutions
import random
import sys
import matplotlib.pyplot as plt
import numpy as np
import time
import ast



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
    csv = f"./data/gameboards/Rushhour{board_sizes[board_number]}x{board_sizes[board_number]}_{board_number}.csv"
    data = [size, csv]

    # --------------------------- Random algorithm --------------------------
    if algorithm == "random":     
        # get input number of attempts and max moves
        number_of_attempts = int(input("Number of attempts: "))  
        max_moves = int(input("Maximum number of moves: ")) 
        log = True if input("Log solutions (y/n):") == "y" else False
        
        # run random algorithm
        start = time.time()
        solutions = random_main(data, number_of_attempts, max_moves)
        end = time.time()
        print(f"runtime: {round(end - start,2)} seconds") 

        # save logged moves and print length of each solution
        for solution in solutions:
            if log:
                save_log(solution, f"random_board{str(board_number)}")
            print(f"solution of length {len(solution)} found.")     


    # --------------------------- Optimalisation algorithm --------------------------
    elif algorithm == "optimalisation":
        # get input number of attempts and max moves
        number_of_attempts = int(input("Number of attempts: "))  
        max_moves = int(input("Maximum number of moves: ")) 
        animation = True if input("Create animation from solution (y/n):") == "y" else False
        log = True if input("Log solutions (y/n):") == "y" else False

        # run random algorithm
        start = time.time()
        solutions = random_main(data, number_of_attempts, max_moves)
        
        # run optimalisation algorithm
        short_solutions = improve_solutions(solutions, data, animation=animation, log=log)
        
        end = time.time()
        print(f"runtime: {round(end - start,2)} seconds")

    # --------------------------- Depth first algorithm --------------------------
    elif algorithm == "depth_first":
        # get all function parameters from user
        fixed_solutions = True if input("Create fixed number of solutions (y/n):") == "y" else False
        if fixed_solutions:
            number_of_attempts = int(input("number of solutions (int):"))
        else:
            number_of_attempts = int(input("number of runs (int):"))
        branch_and_bound = True if input("Use dynamic bound for depth (y/n):") == "y" else False
        max_moves = int(input("Maximum number of moves: "))
        randomize = True if input("Randomize order of search (y/n):") == "y" else False
        filter_movesets = input("Filter with solution movesets (None/solution movesets):")
        if filter_movesets == "None":
            filter_movesets = None
        else:
            # interpret str as list
            filter_movesets = ast.literal_eval(filter_movesets)

        # run algorithm
        start = time.time()
        solutions = depth_first_smart_archive_main(number_of_attempts, max_moves, data, fixed_solutions=fixed_solutions, branch_and_bound = branch_and_bound, randomize = randomize, filter_movesets = filter_movesets)
        end = time.time()
        print(f"runtime: {round(end - start,2)} seconds") 

        log = True if input("Log solutions (y/n):") == "y" else False
        
        # print solutions and log if requested
        if len(solutions):
            for i in range(len(solutions)):
                if log:
                    save_log(solutions[i], str(board_number)+"_"+str(i))
                print(f"solution of length {len(solutions[i])} found: {solutions[i]}")
        else:
            print("no solution was found")
          


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

        max_moves_board = { "1": 287, "2": 167, "3": 2680,
                            "4": 2889, "5": 4441, "6": 1691, "7": 6000}

        number_of_attempts = int(input("number of attempts:"))
        plot = input("plot Y/N:")
        if plot.capitalize() == "Y":
            plot = True
        else:
            plot = False

        max_moves = max_moves_board[board_number]
        
        start = time.time()
    
        start = begin = time.time()
        solutions = random_main(data, number_of_attempts, max_moves)
        print(solutions)
        end = time.time()
        print(f"time to find solutions: {round(end - start,2)} seconds")

        start = time.time()
        short_solutions = improve_solutions(solutions[0], data, animation=False, log=False)
        end = time.time()
        print(f"time to optimize solution: {round(end - start,2)} seconds")
        print(f"Total time: {round(end - begin,2)} seconds")

        if plot:
            bar_plot_of_solutions(short_solutions, board_number, number_of_attempts)
        
     
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
        print("Invalid algorithm input. Choose: random, optimalisation, or depth_first")
        sys.exit(0)
