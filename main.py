from code.classes.board import Board
from code.classes.car import Car
from code.classes.board import make_animation, save_log
from code.algorithms.random import random_algorithm
from code.algorithms.depth_first_first_jeroen import depth_first_algorithm, check_solution, depth_first_main, remove_useless_moves
from code.algorithms.breadth_first_Tünde import breadth_first_algorithm
import random
import sys
import matplotlib.pyplot as plt
import numpy as np

#random_algorithm(20)

board_number = "1"
board_sizes = { "1": 6, "2": 6, "3": 6,
                 "4": 9, "5": 9, "6": 9,
                 "7": 12, "test" : 4}

data = f"./data/gameboards/Rushhour{board_sizes[board_number]}x{board_sizes[board_number]}_{board_number}.csv"
#game = Board(board_sizes[board_number],data)
#game.draw_board()

number_of_attempts = 10
max_moves = 60
size = board_sizes[board_number]
solutions = depth_first_main(number_of_attempts, max_moves, size, data, True)
#solutions = [[['A', -1], ['C', -1], ['G', 1], ['L', 1], ['B', -1], ['J', -1], ['B', 1], ['A', 1], ['I', -2], ['A', -1], ['H', 1], ['A', 1], ['E', -1], ['D', -1], ['A', -1], ['G', 1], ['D', 1], ['L', 1], ['J', -2], ['D', -1], ['E', -2], ['D', 1], ['H', -1], ['D', -1], ['I', 1], ['I', 1], ['I', 1], ['H', 1], ['E', 1], ['E', 1], ['J', 1], ['J', 1], ['J', 1], ['L', -2], ['J', -1], ['F', 1], ['X', 1], ['F', -1], ['J', 1], ['F', 1], ['E', -1], ['K', 2], ['E', -1], ['F', 1], ['X', 1], ['K', -2], ['X', 1], ['K', 2], ['G', -1], ['K', -2], ['B', -1], ['F', -2], ['I', 1], ['X', 1]]]
#print(solutions[0])

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
#random_algorithm(1000)

#print(sys.getrecursionlimit())

board_number = "1"
board_sizes = { "1": 6, "2": 6, "3": 6,
                "4": 9, "5": 9, "6": 9,
                "7": 12}

data = f"./data/gameboards/Rushhour{board_sizes[board_number]}x{board_sizes[board_number]}_{board_number}.csv"
game = Board(board_sizes[board_number],data)
game.load_board()
shortest, lengths = breadth_first_algorithm(game)
make_animation(shortest, board_sizes[board_number], data)
print(len(lengths)," solutions were found.")

lengths = np.array(lengths)
range_lengths = range(np.min(lengths), np.max(lengths)) 
height = np.zeros(len(range_lengths))

for i in range(len(range_lengths)):
    height[i] = np.count_nonzero(lengths == range_lengths[i])
    print(f"there are {height[i]} solutions of length {range_lengths[i]}")

# print(range_lengths, height)
# plt.plot(np.array(range_lengths),height)
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# ax.bar(np.array(range_lengths), height)
# fig.show()




# print(board.find_moves())


# while True:
#     move = input("Car:")

#     if move == "q":
#         break
#     step = int(input("Step: "))
#     if move not in board.cars.keys():
#         print("Invalid car")
#     elif board.validate_move(move, step):
#         board.move(move, step)
#         board.log_move(move, step)
#         board.draw_board()
#         print(board.find_moves())
#         if board.won():
#             print("Game was won")
#             break
#     else:
#         print("Invalid move")
    
# make_animation(board.moves, board.size, data)
# #board.save_log()
# print("Game ended")
     

