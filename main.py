from code.classes.board import Board
from code.classes.car import Car


data = "./data/gameboards/Rushhour6x6_1.csv"
board = Board(6,data)

board.load_board()
print(board.draw_board())

board.move("A",-1)
board.move("C",-1)
board.move("J",-1)
board.move("I",-2)
print(board.draw_board())