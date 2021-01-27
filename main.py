from code.classes.board import Board
from code.classes.car import Car
from code.util import make_animation, save_log, bar_plot_of_solutions
from code.algorithms.random import random_main
from code.algorithms.depth_first import depth_first_main
from code.algorithms.improve_solution import improve_solutions
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
        number_of_attempts = int(input("Number of solutions (int): "))  
        max_moves = int(input("Maximum number of moves (int): ")) 
        log = True if input("Log solutions (y/n):").capitalize() == "Y" else False
        
        # run random algorithm
        start = time.time()
        solutions = random_main(data, number_of_attempts, max_moves)
        end = time.time()
        print(f"runtime: {round(end - start,2)} seconds") 

        # save logged moves and print length of each solution
        for i in range(len(solutions)):
            if log:
                save_log(solutions[i], f"random_board{str(board_number)}_{str(i)}")
            print(f"solution of length {len(solutions[i])} found.")    


    # --------------------------- Optimalisation algorithm --------------------------
    elif algorithm == "optimalisation":
        # get input for parameters of algorithm
        number_of_attempts = int(input("Number of solutions (int): "))  
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
        max_moves = int(input("Maximum number of moves: "))
        branch_and_bound = True if input("Use dynamic bound for depth (y/n):") == "y" else False
        print_all = True if input("Print all solutions (y/n):") == "y" else False
        log = True if input("Log best solution (y/n):") == "y" else False
        animation = True if input("Animate best solution (y/n):") == "y" else False
        filter_movesets = input("Filter with solution movesets (None/solution movesets):")
        if filter_movesets == "None":
            filter_movesets = None
        else:
            # interpret str as list
            filter_movesets = ast.literal_eval(filter_movesets)

        # run algorithm
        start = time.time()
        solution = depth_first_main(max_moves, data, branch_and_bound = branch_and_bound, filter_movesets = filter_movesets, print_all = print_all)
        end = time.time()
        print(f"runtime: {round(end - start,2)} seconds") 

        # print best solution and log if requested
        if len(solution):
            print(f"best solution ({len(solution)} moves): {solution}")
            if log:
                save_log(solution, "depth_first"+board_number)
            if animation:
                make_animation(solution, data, "depth_first"+board_number)
        else:
            print("no solution found")

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

        save_log(game.moves, f"gameplay_board_{board_number}")
        print("Game ended")

    # ------------------------------------------------------------------------
    else:
        print("Invalid algorithm input. Choose: random, optimalisation, depth_first, or play")
        sys.exit(0)
