from code.classes.board import Board
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
        possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
        if 0 in possible_steps:
            possible_steps.remove(0)
        
        step = random.choice(possible_steps)
        
        game.move(car, step)
        game.log_move(car, step)
        game.draw_board()
        # current_move += 1
        
        if game.won():
            break

    game.save_log()