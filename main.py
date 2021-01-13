from code.classes.board import Board
from code.classes.car import Car
from code.classes.board import make_animation
from code.algorithms.random import random_algorithm
from code.algorithms.breadth_first_Tünde import breadth_first_algorithm
import random
import sys
import matplotlib.pyplot as plt
import numpy as np

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

# board.load_board()
# board.draw_board()

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
     

