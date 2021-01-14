from code.classes.board import Board, make_animation
import random

def random_algorithm(game):
    """ algorithm that performs a random move out of the possible moves on the board
        it repeats this until the game is won and saves the moves in a csv-file
        takes a game of type Board object as input """
    
    game.load_board()

    # repeat until game is won
    while True:
        # find possible moves and select random car to move
        possible_moves = game.find_moves()
        car = random.choice(list(possible_moves.keys()))

        # select range of car, excluding 0, and select random step out of range
        possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
        if 0 in possible_steps:
            possible_steps.remove(0)
        step = random.choice(possible_steps)
        
        # move car and log move
        game.move(car, step)
        game.log_move(car, step)
        
        # break out of loop if game is won
        if game.won():
            break

    # save logged moves and create animation of moves
    game.save_log()
    # make_animation(game.moves, game.size, data)