from code.classes.board import Board
from code.classes.car import Car
from code.classes.board import make_animation
from code.algorithms.random import random_algorithm
from code.algorithms.depth_first_Tünde import depth_first
import random

#random_algorithm(1000)

depth_first(6, 6, "./data/gameboards/Rushhour6x6_1.csv")

# board_number = "1"
# board_sizes = { "1": 6, "2": 6, "3": 6,
#                 "4": 9, "5": 9, "6": 9,
#                 "7": 12}

# data = f"./data/gameboards/Rushhour{board_sizes[board_number]}x{board_sizes[board_number]}_{board_number}.csv"
# board = Board(board_sizes[board_number],data)

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
     

