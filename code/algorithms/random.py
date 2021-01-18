from code.classes.board import Board, make_animation
import copy
import random

class Random_algorithm:

    def __init__(self, size, data):
        self.size = size
        self.data = data
        self.length_best_solution = float('inf')
        self.best_solution = []
        self.winning_hash = ''

    def run(self, number_of_attempts, max_moves):
        solutions = []
        for i in range(number_of_attempts):
            self.length_best_solution = float('inf')
            self.best_solution = []
            while self.length_best_solution > max_moves:
                game = Board(self.size, self.data)
                new_solution = self.random_moves(game)
                # print(new_solution)
                if len(new_solution) < self.length_best_solution:
                    self.length_best_solution = len(new_solution)

            self.best_solution = copy.deepcopy(new_solution)
            solutions.append(self.best_solution)
        return solutions


    def random_moves(self, game):
        # repeat until game is won
        while not game.won():
            
            # find possible moves and select random car to move
            possible_moves = game.find_moves()
            car = random.choice(list(possible_moves.keys()))

            # select range of car, excluding 0, and select random step out of range
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)
            step = random.choice(possible_steps)

            if len(game.moves) == 0:
                game.move(car, step)
                game.log_move(car, step)
            elif game.moves[-1][0] == car and game.moves[-1][1] == -step:
                # print("skipped step")
                pass
            else:
                game.move(car, step)
                game.log_move(car, step)

            if len(game.moves) >= self.length_best_solution:
                break

        # save logged moves and create animation of moves
        # self.game.save_log()
        # make_animation(game.moves, game.size, data)

        self.winning_hash = game.give_hash()

        return game.moves

    def get_winning_hash(self):
        return self.winning_hash