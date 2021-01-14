from code.classes.board import Board, make_animation
import random

class Random_algorithm:

    def __init__(self, game, data):
        self.game = game
        self.game.load_board()
        self.data = data

    def run(self):
        # repeat until game is won
        while not self.game.won():
            
            # find possible moves and select random car to move
            possible_moves = self.game.find_moves()
            car = random.choice(list(possible_moves.keys()))

            # select range of car, excluding 0, and select random step out of range
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)
            step = random.choice(possible_steps)
            
            # move car and log move
            self.game.move(car, step)
            self.game.log_move(car, step)

        # save logged moves and create animation of moves
        self.game.save_log()
        # make_animation(game.moves, game.size, data)