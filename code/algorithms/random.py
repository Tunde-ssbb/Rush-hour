from code.classes.board import Board
import random

def random(moves):
    data = "./data/gameboards/Rushhour6x6_1.csv"
    game = Board(6, data)

    game.load_board()

    current_move = 0

    while current_move < moves:
        possible_moves = game.find_moves()
        car = random.choice(possible_moves.keys())
        step = random.randrange(possible_moves[car][0], possible_moves[car][1])
        game.move(car, step)
        game.log_move(car, step)

        if game.won():
            break

    game.save_log()