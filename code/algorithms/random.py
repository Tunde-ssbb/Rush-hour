from code.classes.board import Board
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
        """
        Function used to call random_moves algorithm number of attempts times.
        Keeps running until length of solution is smaller than max moves.
        Input: number_of_attempts (int), max_moves (int). Output: list of solution movesets.
        """
        solutions = []
        for i in range(number_of_attempts):
            print(f"finding random solution {len(solutions) + 1}")
            
            # reset length and best solution to initial values
            self.length_best_solution = float('inf')
            self.best_solution = []

            # repeat random algorithm until smaller solution than max moves is found
            while self.length_best_solution > max_moves:
                game = Board(self.size, self.data)
                new_solution = self.random_moves(game)
                
                # replace length best solution if new solution is smaller
                if len(new_solution) < self.length_best_solution:
                    self.length_best_solution = len(new_solution)

            # if solution found copy moves and add to solutions list
            self.best_solution = copy.deepcopy(new_solution)
            solutions.append(self.best_solution)

        return solutions


    def random_moves(self, game):
        """
        Random algorithm that finds solutions by performing random moves. 
        Keeps running until game is won.
        Input: game (Board object). Output: list of moves.
        """

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

            # filter out moves that are the exact opposite of the last move
            if len(game.moves) == 0:
                game.move(car, step)
                game.log_move(car, step)
            elif game.moves[-1][0] == car and game.moves[-1][1] == -step:
                pass
            else:
                game.move(car, step)
                game.log_move(car, step)

            if len(game.moves) >= self.length_best_solution:
                break

        
        # save hash of winning board instance
        self.winning_hash = game.give_hash()

        return game.moves

    def get_winning_hash(self):
        """
        Gives hash of winning board instance.
        """
        return self.winning_hash