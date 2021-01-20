from code.classes.board import Board
from code.classes.car import Car
from code.util import make_animation, save_log, get_cars
from code.algorithms.random import Random_algorithm
from code.algorithms.depth_first import depth_first_algorithm, depth_first_main
from code.algorithms.improve_solution import improve_solutions
from code.algorithms.breadth_first_Tünde import breadth_first_algorithm
from code.heuristics.winning_comparison import winning_comparison
import random
import sys
import matplotlib.pyplot as plt
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
        short_solutions = improve_solutions(solutions, size, data, animation=False, log=False)

    # --------------------------- depth algorithm --------------------------
    elif algorithm == "depth_first":
        number_of_attempts = int(input("Number of attempts: "))
        # max_moves = int(input("Maximum number of moves: "))
        random = Random_algorithm(size, data)
        max_moves = len(random.run(1, 100)[0])
        # while max_moves > 1000:
        #     max_moves = random.run(10)
        print(f"random steps: {max_moves}")
        solutions = depth_first_main(number_of_attempts, max_moves, size, data, True)
        print("starting optimalization")
        short_solutions = improve_solutions(solutions, size, data, animation=True, log=True)
        """
        number_correct_solutions = 0
        for solution in short_solutions:
            if len(solution) == 15:
                number_correct_solutions += 1

        print(f"{number_correct_solutions} solutions out of {number_of_attempts} are the best solution")
        """




    # --------------------------- breadth algorithm --------------------------
    elif algorithm == "breadth_first":
        game = Board(size, data)
        game.load_board()
        shortest, lengths = breadth_first_algorithm(game)
        make_animation(shortest, board_sizes[board_number], data)
        print(len(lengths)," solutions were found.")


    # ------------------------------------------------------------------------
    elif algorithm == "test_improve_solution":
        number_of_attempts = 100
        max_moves = 2000
        random = Random_algorithm(size, data)

        start = time.time()
    
        start = begin = time.time()
        solutions = random.run(number_of_attempts, max_moves)
        end = time.time()
        print(f"time to find a solution: {round(end - start,2)} seconds")

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
            


        plt.figure(1)
        plt.bar(lengths,heights)
        plt.xlabel("number of moves")
        plt.xticks(lengths)
        plt.savefig(f'100solutions_of_board{board_number}.png')


    # ------------------------------------------------------------------------        
    elif algorithm == "check":
        random = Random_algorithm(size, data)
        random.run(1)
        winning_hash = random.get_winning_hash()
        
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
                
                score = winning_comparison(board, winning_hash)
                print(score)

                if board.won():
                    print("Game was won")
                    break
            else:
                print("Invalid move")
            
        board.save_log()
        print("Game ended")

    # ------------------------------------------------------------------------
    else:
        print("Invalid algorithm input. Choose: random, depth_first, or breadth_first")
        sys.exit(0)
