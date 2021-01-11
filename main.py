from code.classes.board import Board
from code.classes.car import Car


data = "./data/gameboards/Rushhour6x6_1.csv"
board = Board(6,data)

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
        board.find_moves()
        if board.won():
            print("Game was won")
            break
    else:
        print("Invalid move")
    

board.save_log()
print("Game ended")
     

