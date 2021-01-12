from code.classes.board import Board, make_animation
import random

def random_algorithm(moves):
    data = "./data/gameboards/Rushhour6x6_1.csv"
    game = Board(6, data)

    game.load_board()
    game.draw_board()

    current_move = 0

    while current_move < moves:
        possible_moves = game.find_moves()
        car = random.choice(list(possible_moves.keys()))
        step = random.randrange(possible_moves[car][0], possible_moves[car][1])
        if step != 0:
            game.move(car, step)
            game.log_move(car, step)
            game.draw_board()
            current_move += 1
        
        if game.won():
            break

    game.save_log()
    make_animation(game.moves, game.size, data)