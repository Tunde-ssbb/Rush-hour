from code.classes.board import Board
from code.classes.car import Car
from code.util import make_animation, save_log, bar_plot_of_solutions
from code.algorithms.random import random_main
from code.algorithms.depth_first import depth_first_main
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
        animation = True if input("Create animation from solution (y/n):").capitalize() == "Y" else False
        log = True if input("Log solutions (y/n):").capitalize() == "Y" else False
        plot = True if input("Plot solutions y/n:").capitalize() == "Y" else False
        
        max_moves_board = { "1": 287, "2": 167, "3": 2680,
                            "4": 2889, "5": 4441, "6": 1691, "7": 6000}
        max_moves = max_moves_board[board_number]

        # run random algorithm
        start = time.time()
        solutions = random_main(data, number_of_attempts, max_moves)
        
        # run optimalisation algorithm
        short_solutions = improve_solutions(solutions, data, animation=animation, log=log)
        
        end = time.time()
        print(f"runtime: {round(end - start,2)} seconds")
        if plot:
            bar_plot_of_solutions(short_solutions, board_number, number_of_attempts)

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
        log = True if input("Log solutions (y/n):") == "y" else False
        filter_movesets = input("Filter with solution movesets (None/solution movesets):")
        if filter_movesets == "None":
            filter_movesets = None
        else:
            # interpret str as list
            filter_movesets = ast.literal_eval(filter_movesets)

        # run algorithm
        start = time.time()
        solutions = depth_first_main(number_of_attempts, max_moves, data, fixed_solutions=fixed_solutions, branch_and_bound = branch_and_bound, randomize = randomize, filter_movesets = filter_movesets)
        end = time.time()
        print(f"runtime: {round(end - start,2)} seconds") 

        
        
        # print solutions and log if requested
        if len(solutions):
            for i in range(len(solutions)):
                if log:
                    save_log(solutions[i], str(board_number)+"_"+str(i))
                print(f"solution of length {len(solutions[i])} found: {solutions[i]}")
        else:
            print("no solution was found")

    # ------------------------------------------------------------------------        
    elif algorithm == "play":
        
        # create game and draw board
        game = Board(data)
        game.draw_board()

        # repeat until game is won
        while not game.won():
            
            # ask for car to move and check if car is valid
            move = input("Car:")
            if move not in game.cars.keys():
                print("Invalid car")

            # quit game
            if move == "q":
                break
            
            # ask for step input
            step = int(input("Step: "))
            
            # if valid move, move car, log move and draw new board
            if game.validate_move(move, step):
                game.move(move, step)
                game.log_move(move, step)
                game.draw_board()         
            
            else:
                print("Invalid move")


        if game.won():
            print("Game was won")

        game.save_log()
        print("Game ended")

    # ------------------------------------------------------------------------
    else:
        print("Invalid algorithm input. Choose: random, optimalisation, depth_first, or play")
        sys.exit(0)
